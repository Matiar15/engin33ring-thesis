import { useReducer, useCallback, useRef, useEffect, ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';
import { VideoAnalysisContext } from './VideoAnalysisContext.tsx';
import { videoAnalysisReducer, initialVideoAnalysisState } from './videoAnalysisReducer.ts';
import { generateMockDetection, generateMockBoundingBox } from '@/features/analysis/mocks';

interface VideoAnalysisProviderProps {
  children: ReactNode;
}

export function VideoAnalysisProvider({ children }: VideoAnalysisProviderProps) {
  const navigate = useNavigate();
  const [state, dispatch] = useReducer(videoAnalysisReducer, initialVideoAnalysisState);

  const processingStartTime = useRef<Date | null>(null);
  const detectionInterval = useRef<NodeJS.Timeout | null>(null);
  const boxInterval = useRef<NodeJS.Timeout | null>(null);

  // Mock detection simulation - TODO: replace with real API/WebSocket
  useEffect(() => {
    if (!state.isProcessing) {
      if (detectionInterval.current) {
        clearInterval(detectionInterval.current);
        detectionInterval.current = null;
      }
      return;
    }

    detectionInterval.current = setInterval(() => {
      if (Math.random() > 0.4) {
        dispatch({ type: 'ADD_DETECTION', payload: generateMockDetection() });
      }
    }, 800 + Math.random() * 1200);

    return () => {
      if (detectionInterval.current) {
        clearInterval(detectionInterval.current);
      }
    };
  }, [state.isProcessing]);

  // Mock bounding boxes simulation - TODO: replace with real API/WebSocket
  useEffect(() => {
    if (!state.isProcessing) {
      if (boxInterval.current) {
        clearInterval(boxInterval.current);
        boxInterval.current = null;
      }
      return;
    }

    boxInterval.current = setInterval(() => {
      if (Math.random() > 0.6) {
        const newBoxes = [generateMockBoundingBox()];
        if (Math.random() > 0.7) {
          newBoxes.push(generateMockBoundingBox());
        }
        dispatch({ type: 'SET_BOUNDING_BOXES', payload: newBoxes });
      }
    }, 150);

    return () => {
      if (boxInterval.current) {
        clearInterval(boxInterval.current);
      }
    };
  }, [state.isProcessing]);

  const selectVideo = useCallback((file: File, url: string) => {
    dispatch({ type: 'SELECT_VIDEO', payload: { file, url } });
    processingStartTime.current = new Date();
  }, []);

  const pause = useCallback(() => {
    dispatch({ type: 'PAUSE' });
  }, []);

  const resume = useCallback(() => {
    dispatch({ type: 'RESUME' });
  }, []);

  const stopAndArchive = useCallback(() => {
    dispatch({ type: 'STOP' });

    if (detectionInterval.current) {
      clearInterval(detectionInterval.current);
    }

    const endTime = new Date();
    const startTime = processingStartTime.current || endTime;
    const durationMs = endTime.getTime() - startTime.getTime();
    const durationSecs = Math.floor(durationMs / 1000);
    const mins = Math.floor(durationSecs / 60);
    const secs = durationSecs % 60;

    // TODO: Send to API
    console.log('Archiving session:', {
      thumbnail: state.videoUrl || '',
      date: startTime,
      duration: `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`,
      signsDetected: state.detectionLogs.length,
      detections: state.detectionLogs,
    });

    navigate('/registry');
  }, [state.videoUrl, state.detectionLogs, navigate]);

  const reset = useCallback(() => {
    if (state.videoUrl) {
      URL.revokeObjectURL(state.videoUrl);
    }
    if (detectionInterval.current) {
      clearInterval(detectionInterval.current);
    }
    if (boxInterval.current) {
      clearInterval(boxInterval.current);
    }
    dispatch({ type: 'RESET' });
  }, [state.videoUrl]);

  const value = {
    state,
    selectVideo,
    pause,
    resume,
    stopAndArchive,
    reset,
  };

  return (
    <VideoAnalysisContext.Provider value={value}>
      {children}
    </VideoAnalysisContext.Provider>
  );
}
