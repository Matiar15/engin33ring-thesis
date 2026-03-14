import { DetectionLog, BoundingBox } from '@/features/analysis/types';

// State
export interface VideoAnalysisState {
  videoFile: File | null;
  videoUrl: string | null;
  isProcessing: boolean;
  detectionLogs: DetectionLog[];
  boundingBoxes: BoundingBox[];
}

export const initialVideoAnalysisState: VideoAnalysisState = {
  videoFile: null,
  videoUrl: null,
  isProcessing: false,
  detectionLogs: [],
  boundingBoxes: [],
};

// Actions
export type VideoAnalysisAction =
  | { type: 'SELECT_VIDEO'; payload: { file: File; url: string } }
  | { type: 'ADD_DETECTION'; payload: DetectionLog }
  | { type: 'SET_BOUNDING_BOXES'; payload: BoundingBox[] }
  | { type: 'PAUSE' }
  | { type: 'RESUME' }
  | { type: 'STOP' }
  | { type: 'RESET' };

// Reducer
export function videoAnalysisReducer(
  state: VideoAnalysisState,
  action: VideoAnalysisAction
): VideoAnalysisState {
  switch (action.type) {
    case 'SELECT_VIDEO':
      return {
        ...state,
        videoFile: action.payload.file,
        videoUrl: action.payload.url,
        isProcessing: true,
        detectionLogs: [],
        boundingBoxes: [],
      };
    case 'ADD_DETECTION':
      return {
        ...state,
        detectionLogs: [...state.detectionLogs, action.payload],
      };
    case 'SET_BOUNDING_BOXES':
      return {
        ...state,
        boundingBoxes: action.payload,
      };
    case 'PAUSE':
      return {
        ...state,
        isProcessing: false,
      };
    case 'RESUME':
      return {
        ...state,
        isProcessing: true,
      };
    case 'STOP':
      return {
        ...state,
        isProcessing: false,
        boundingBoxes: [],
      };
    case 'RESET':
      return initialVideoAnalysisState;
    default:
      return state;
  }
}

