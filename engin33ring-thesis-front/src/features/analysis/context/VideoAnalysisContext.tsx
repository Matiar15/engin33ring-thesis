import { createContext, useContext } from 'react';
import { VideoAnalysisState } from './videoAnalysisReducer';

// Context Value
export interface VideoAnalysisContextValue {
  state: VideoAnalysisState;
  selectVideo: (file: File, url: string) => void;
  pause: () => void;
  resume: () => void;
  stopAndArchive: () => void;
  reset: () => void;
}

// Context
export const VideoAnalysisContext = createContext<VideoAnalysisContextValue | null>(null);

// Hook
export function useVideoAnalysis() {
  const context = useContext(VideoAnalysisContext);

  if (!context) {
    throw new Error('useVideoAnalysis must be used within VideoAnalysisProvider');
  }

  return context;
}

// Re-export types for convenience
export type { VideoAnalysisState, VideoAnalysisAction } from './videoAnalysisReducer';

