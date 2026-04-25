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
  const videoRef = useRef<HTMLVideoElement>(null);

  const { analysisId, startAnalysis, endAnalysis, resetAnalysis } = useAnalysisLifecycle(userId);

  const onFrameUploaded = useCallback((data: any) => {
    const isDetection = data.sign && data.sign !== "NO_DETECTION";

    if (isDetection) {
      dispatch({
        type: 'ADD_DETECTION',
        payload: {
          id: Math.random().toString(36).substr(2, 9),
          timestamp: new Date(),
          signType: data.sign,
          confidence: data.confidence,
        },
      });
    }

    if (isDetection && data.bounding_box) {
      dispatch({
        type: 'SET_BOUNDING_BOXES',
        payload: [{
          id: Math.random().toString(36).substr(2, 9),
          x: data.bounding_box.x,
          y: data.bounding_box.y,
          width: data.bounding_box.width,
          height: data.bounding_box.height,
          label: data.sign,
          color: '#ef4444',
        }],
      });
    } else {
      dispatch({ type: 'SET_BOUNDING_BOXES', payload: [] });
    }
  }, [dispatch]);

  const { resetFrameCounter } = useFrameUploader({
    isProcessing: state.isProcessing,
    videoRef,
    analysisId,
    userId,
    onFrameUploaded,
  });

  const selectVideo = useCallback(async (file: File, url: string) => {
    const newAnalysisId = await startAnalysis();
    if (!newAnalysisId) return;

    resetFrameCounter();
    dispatch({ type: 'SELECT_VIDEO', payload: { file, url } });
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
    dispatch({ type: 'SAVE_START' });

    try {
      await endAnalysis();
      navigate('/registry');
    } catch (error) {
      console.error('Failed to save analysis:', error);
      dispatch({ type: 'SAVE_DONE' });
    }
  }, [navigate, endAnalysis]);

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
    videoRef,
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
