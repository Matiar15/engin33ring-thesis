import { describe, it, expect } from 'vitest';
import {
  videoAnalysisReducer,
  initialVideoAnalysisState,
} from '@/features/analysis/context/videoAnalysisReducer';

const sampleDetection = {
  id: 'd1',
  timestamp: new Date('2025-01-01T10:00:00Z'),
  signType: 'Stop Sign',
  confidence: 95,
};

const sampleBox = {
  id: 'b1',
  x: 10,
  y: 20,
  width: 30,
  height: 40,
  label: 'Stop Sign',
  color: '#00FF88',
};

describe('videoAnalysisReducer', () => {
  it('handles SELECT_VIDEO', () => {
    const next = videoAnalysisReducer(initialVideoAnalysisState, {
      type: 'SELECT_VIDEO',
      payload: { file: new File(['x'], 'clip.mp4', { type: 'video/mp4' }), url: 'blob:video' },
    });

    expect(next.videoFile).not.toBeNull();
    expect(next.videoUrl).toBe('blob:video');
    expect(next.isProcessing).toBe(true);
    expect(next.detectionLogs).toHaveLength(0);
    expect(next.boundingBoxes).toHaveLength(0);
  });

  it('handles ADD_DETECTION', () => {
    const next = videoAnalysisReducer(initialVideoAnalysisState, {
      type: 'ADD_DETECTION',
      payload: sampleDetection,
    });

    expect(next.detectionLogs).toHaveLength(1);
    expect(next.detectionLogs[0]).toEqual(sampleDetection);
  });

  it('handles SET_BOUNDING_BOXES', () => {
    const next = videoAnalysisReducer(initialVideoAnalysisState, {
      type: 'SET_BOUNDING_BOXES',
      payload: [sampleBox],
    });

    expect(next.boundingBoxes).toHaveLength(1);
    expect(next.boundingBoxes[0]).toEqual(sampleBox);
  });

  it('handles PAUSE/RESUME', () => {
    const paused = videoAnalysisReducer({
      ...initialVideoAnalysisState,
      isProcessing: true,
    }, { type: 'PAUSE' });

    expect(paused.isProcessing).toBe(false);

    const resumed = videoAnalysisReducer(paused, { type: 'RESUME' });
    expect(resumed.isProcessing).toBe(true);
  });

  it('handles STOP and clears bounding boxes only', () => {
    const state = {
      ...initialVideoAnalysisState,
      isProcessing: true,
      detectionLogs: [sampleDetection],
      boundingBoxes: [sampleBox],
    };

    const next = videoAnalysisReducer(state, { type: 'STOP' });

    expect(next.isProcessing).toBe(false);
    expect(next.boundingBoxes).toHaveLength(0);
    expect(next.detectionLogs).toHaveLength(1);
  });

  it('handles RESET', () => {
    const state = {
      ...initialVideoAnalysisState,
      isProcessing: true,
      detectionLogs: [sampleDetection],
      boundingBoxes: [sampleBox],
    };

    const next = videoAnalysisReducer(state, { type: 'RESET' });

    expect(next).toEqual(initialVideoAnalysisState);
  });
});

