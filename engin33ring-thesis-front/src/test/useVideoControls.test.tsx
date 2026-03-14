import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { useVideoControls } from '@/features/analysis/hooks/useVideoControls';

const TestHarness = ({ onPlay, onPause }: { onPlay?: () => void; onPause?: () => void }) => {
  const { videoRef, togglePlay, currentTime, progress } = useVideoControls({ onPlay, onPause });

  return (
    <div>
      <video data-testid="video" ref={videoRef} />
      <button type="button" onClick={togglePlay}>Toggle</button>
      <span data-testid="time">{currentTime}</span>
      <span data-testid="progress">{progress}</span>
    </div>
  );
};

describe('useVideoControls', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('togglePlay calls play and pause', () => {
    render(<TestHarness />);
    const video = screen.getByTestId('video') as HTMLVideoElement;

    video.play = vi.fn().mockResolvedValue(undefined);
    video.pause = vi.fn();

    fireEvent.click(screen.getByText('Toggle'));
    expect(video.play).toHaveBeenCalledTimes(1);

    fireEvent.play(video);
    fireEvent.click(screen.getByText('Toggle'));
    expect(video.pause).toHaveBeenCalledTimes(1);
  });

  it('updates progress and currentTime on timeupdate', () => {
    render(<TestHarness />);
    const video = screen.getByTestId('video') as HTMLVideoElement;

    Object.defineProperty(video, 'duration', { value: 120, writable: true });
    Object.defineProperty(video, 'currentTime', { value: 60, writable: true });

    fireEvent.timeUpdate(video);

    expect(screen.getByTestId('time')).toHaveTextContent('1:00');
    expect(screen.getByTestId('progress')).toHaveTextContent('50');
  });

  it('fires onPlay/onPause callbacks', () => {
    const onPlay = vi.fn();
    const onPause = vi.fn();

    render(<TestHarness onPlay={onPlay} onPause={onPause} />);
    const video = screen.getByTestId('video') as HTMLVideoElement;

    fireEvent.play(video);
    fireEvent.pause(video);

    expect(onPlay).toHaveBeenCalledTimes(1);
    expect(onPause).toHaveBeenCalledTimes(1);
  });
});
