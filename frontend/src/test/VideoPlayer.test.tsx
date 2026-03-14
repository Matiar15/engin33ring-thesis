import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import VideoPlayer from '@/features/analysis/components/VideoPlayer.tsx';

vi.mock('@/features/analysis/context', () => ({
  useVideoAnalysis: () => ({
    state: { boundingBoxes: [] },
    pause: vi.fn(),
    resume: vi.fn(),
  }),
}));

vi.mock('@/features/analysis/hooks/useBoundingBoxOverlay', () => ({
  useBoundingBoxOverlay: () => ({ canvasRef: { current: null } }),
}));

vi.mock('@/features/analysis/hooks/useVideoControls', () => ({
  useVideoControls: () => ({
    videoRef: { current: null },
    containerRef: { current: null },
    isPlaying: false,
    isMuted: true,
    progress: 0,
    currentTime: '0:00',
    duration: '0:00',
    togglePlay: vi.fn(),
    toggleMute: vi.fn(),
    toggleFullscreen: vi.fn(),
  }),
}));

describe('VideoPlayer', () => {
  it('renders playback controls', () => {
    render(<VideoPlayer videoUrl="blob:video" isProcessing={false} />);

    expect(screen.getByText('0:00 / 0:00')).toBeInTheDocument();
  });
});

