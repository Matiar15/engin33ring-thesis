import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import AnalysisPage from '@/pages/AnalysisPage.tsx';
import { VideoAnalysisProvider } from '@/features/analysis/context';
import { useAuth } from '@/features/auth/context';

vi.mock('@/features/auth/context');
vi.mock('@/features/analysis/hooks/useAnalysisLifecycle', () => ({
  useAnalysisLifecycle: vi.fn((userId) => ({
    analysisId: userId ? 'mock_analysis_id' : null,
    startAnalysis: vi.fn().mockResolvedValue(userId ? 'mock_analysis_id' : null),
    endAnalysis: vi.fn().mockResolvedValue(true),
    resetAnalysis: vi.fn(),
  })),
}));
vi.mock('@/features/analysis/hooks/useFrameUploader', () => ({
  useFrameUploader: vi.fn(() => ({
    resetFrameCounter: vi.fn(),
  })),
}));

const renderAnalysis = () => {
  vi.mocked(useAuth).mockReturnValue({
    userId: 'user_123',
    isAuthenticated: true,
    token: 'mock_token',
    login: vi.fn(),
    logout: vi.fn(),
  });
  vi.spyOn(console, 'error').mockImplementation(() => {});
  // Mock offsetWidth/Height for canvas resizing
  Object.defineProperty(HTMLElement.prototype, 'offsetWidth', { configurable: true, value: 640 });
  Object.defineProperty(HTMLElement.prototype, 'offsetHeight', { configurable: true, value: 480 });
  return render(
    <MemoryRouter
      initialEntries={["/analysis"]}
      future={{
        v7_startTransition: true,
        v7_relativeSplatPath: true,
      }}
    >
      <Routes>
        <Route
          path="/analysis"
          element={
            <VideoAnalysisProvider>
              <AnalysisPage />
            </VideoAnalysisProvider>
          }
        />
        <Route path="/registry" element={<div>Registry View</div>} />
      </Routes>
    </MemoryRouter>,
  );
};

describe('AnalysisPage integration', () => {
  beforeEach(() => {
    vi.spyOn(Math, 'random').mockReturnValue(0.9);
    vi.stubGlobal('crypto', { randomUUID: () => 'uuid' });
    vi.stubGlobal('URL', {
      createObjectURL: vi.fn(() => 'blob:video'),
      revokeObjectURL: vi.fn(),
    });
    vi.spyOn(HTMLMediaElement.prototype, 'play').mockImplementation(function(this: HTMLMediaElement) {
      Object.defineProperty(this, 'paused', { configurable: true, value: false });
      this.dispatchEvent(new Event('play'));
      return Promise.resolve();
    });
    vi.spyOn(HTMLMediaElement.prototype, 'pause').mockImplementation(function(this: HTMLMediaElement) {
      Object.defineProperty(this, 'paused', { configurable: true, value: true });
      this.dispatchEvent(new Event('pause'));
    });
    vi.spyOn(HTMLMediaElement.prototype, 'canPlayType').mockReturnValue('probably');
    Object.defineProperty(HTMLMediaElement.prototype, 'duration', { configurable: true, value: 100 });
    Object.defineProperty(HTMLMediaElement.prototype, 'currentTime', { configurable: true, value: 0 });
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('uploads a video and shows player + filename', async () => {
    renderAnalysis();

    const input = document.querySelector('input[type="file"]') as HTMLInputElement | null;
    expect(input).not.toBeNull();

    const file = new File(['video'], 'sample.mp4', { type: 'video/mp4' });
    if (input) {
      Object.defineProperty(input, 'files', {
        value: [file],
        configurable: true,
      });
      fireEvent.change(input);
    }

    expect(await screen.findByText('sample.mp4')).toBeInTheDocument();
    expect(document.querySelector('video')).not.toBeNull();
  }, 10000);

  it('toggles processing state on play/pause events', async () => {
    renderAnalysis();

    const input = document.querySelector('input[type="file"]') as HTMLInputElement | null;
    const file = new File(['video'], 'sample.mp4', { type: 'video/mp4' });
    if (input) {
      Object.defineProperty(input, 'files', {
        value: [file],
        configurable: true,
      });
      fireEvent.change(input);
    }

    const indicator = await screen.findByTestId('video-processing-indicator');
    expect(indicator).toBeInTheDocument();

    // Wait for "Processing..." to appear
    await screen.findByTestId('video-processing-indicator');

    const video = document.querySelector('video') as HTMLVideoElement;
    
    // Pause video
    fireEvent.pause(video);

    // Wait for "Paused" to appear
    await waitFor(async () => {
      expect(await screen.findByTestId('video-processing-indicator')).toBeInTheDocument();
    }, { timeout: 5000 });

    // Play video
    fireEvent.play(video);

    // Wait for "Processing..." to appear again
    await waitFor(async () => {
      expect(await screen.findByTestId('video-processing-indicator')).toBeInTheDocument();
    }, { timeout: 5000 });
  }, 10000);

  it('navigates to registry after stop and archive', async () => {
    renderAnalysis();

    const input = document.querySelector('input[type="file"]') as HTMLInputElement | null;
    const file = new File(['video'], 'sample.mp4', { type: 'video/mp4' });
    if (input) {
      Object.defineProperty(input, 'files', {
        value: [file],
        configurable: true,
      });
      fireEvent.change(input);
    }

    const stopButton = await screen.findByRole('button', { name: /stop and archive/i });
    fireEvent.click(stopButton);

    expect(await screen.findByText('Registry View')).toBeInTheDocument();
  }, 10000);
});
