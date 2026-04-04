import { useReducer, useCallback, useRef, ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';
import { VideoAnalysisContext } from './VideoAnalysisContext.tsx';
import { videoAnalysisReducer, initialVideoAnalysisState } from './videoAnalysisReducer.ts';
import { useAuth } from '@/features/auth/context';
import { useAnalysisLifecycle } from '@/features/analysis/hooks/useAnalysisLifecycle';
import { useFrameUploader } from '@/features/analysis/hooks/useFrameUploader';

interface VideoAnalysisProviderProps {
  children: ReactNode;
}

export function VideoAnalysisProvider({ children }: VideoAnalysisProviderProps) {
  const navigate = useNavigate();
  const { userId } = useAuth();
  const [state, dispatch] = useReducer(videoAnalysisReducer, initialVideoAnalysisState);

  const processingStartTime = useRef<Date | null>(null);

  const { analysisId, startAnalysis, endAnalysis, resetAnalysis } = useAnalysisLifecycle(userId);

  const onFrameUploaded = useCallback((data: any) => {
    dispatch({
      type: 'ADD_DETECTION',
      payload: {
        id: Math.random().toString(36).substr(2, 9),
        timestamp: new Date(),
        signType: data.sign,
        confidence: 0.99, // Mock confidence
      },
    });

    dispatch({
      type: 'SET_BOUNDING_BOXES',
      payload: [{
        id: Math.random().toString(36).substr(2, 9),
        x: data.bounding_box.x,
        y: data.bounding_box.y,
        width: 100, // Default width
        height: 100, // Default height
        label: data.sign,
        color: '#ef4444',
      }],
    });
  }, [dispatch]);

  const { resetFrameCounter } = useFrameUploader({
    isProcessing: state.isProcessing,
    videoFile: state.videoFile,
    videoUrl: state.videoUrl,
    analysisId,
    userId,
    onFrameUploaded,
  });

  const selectVideo = useCallback(async (file: File, url: string) => {
    const newAnalysisId = await startAnalysis();
    if (!newAnalysisId) return;

    resetFrameCounter();
    dispatch({ type: 'SELECT_VIDEO', payload: { file, url } });
    processingStartTime.current = new Date();
  }, [startAnalysis, resetFrameCounter]);

  const pause = useCallback(() => {
    dispatch({ type: 'PAUSE' });
  }, []);

  const resume = useCallback(() => {
    dispatch({ type: 'RESUME' });
  }, []);

  const finish = useCallback(() => {
    dispatch({ type: 'FINISH' });
  }, []);

  const stopAndArchive = useCallback(async () => {
    dispatch({ type: 'STOP' });

    const endTime = new Date();
    const startTime = processingStartTime.current || endTime;
    const durationMs = endTime.getTime() - startTime.getTime();
    const durationSecs = Math.floor(durationMs / 1000);
    const mins = Math.floor(durationSecs / 60);
    const secs = durationSecs % 60;

    const success = await endAnalysis();

    if (success) {
      console.log('Archiving session:', {
        analysisId,
        thumbnail: state.videoUrl || '',
        date: startTime,
        duration: `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`,
        signsDetected: state.detectionLogs.length,
        detections: state.detectionLogs,
      });

      navigate('/registry');
    }
  }, [state.videoUrl, state.detectionLogs, navigate, analysisId, endAnalysis]);

  const reset = useCallback(() => {
    if (state.videoUrl) {
      URL.revokeObjectURL(state.videoUrl);
    }
    resetAnalysis();
    resetFrameCounter();
    dispatch({ type: 'RESET' });
  }, [state.videoUrl, resetAnalysis, resetFrameCounter]);

  const value = {
    state,
    selectVideo,
    pause,
    resume,
    finish,
    stopAndArchive,
    reset,
  };

  return (
    <VideoAnalysisContext.Provider value={value}>
      {children}
    </VideoAnalysisContext.Provider>
  );
}
