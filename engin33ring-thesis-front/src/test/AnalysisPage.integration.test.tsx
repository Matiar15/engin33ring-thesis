import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import AnalysisPage from '@/pages/AnalysisPage';
import { VideoAnalysisProvider } from '@/features/analysis/context';

const renderAnalysis = () => {
  return render(
    <MemoryRouter initialEntries={["/analysis"]}>
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
    vi.spyOn(HTMLMediaElement.prototype, 'play').mockResolvedValue();
    vi.spyOn(HTMLMediaElement.prototype, 'pause').mockImplementation(() => {});
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('uploads a video and shows player + filename', async () => {
    renderAnalysis();

    const input = document.querySelector('input[type="file"]') as HTMLInputElement | null;
    expect(input).not.toBeNull();

    const file = new File(['video'], 'sample.mp4', { type: 'video/mp4' });
    fireEvent.change(input as HTMLInputElement, { target: { files: [file] } });

    expect(await screen.findByText('sample.mp4')).toBeInTheDocument();
    expect(document.querySelector('video')).not.toBeNull();
  }, 10000);

  it('toggles processing state on play/pause events', async () => {
    renderAnalysis();

    const input = document.querySelector('input[type="file"]') as HTMLInputElement | null;
    const file = new File(['video'], 'sample.mp4', { type: 'video/mp4' });
    fireEvent.change(input as HTMLInputElement, { target: { files: [file] } });

    const video = document.querySelector('video') as HTMLVideoElement;
    expect(await screen.findByText('Processing')).toBeInTheDocument();

    fireEvent.pause(video);
    const pausedLabels = await screen.findAllByText('Paused');
    expect(pausedLabels.length).toBeGreaterThan(0);

    fireEvent.play(video);
    expect(await screen.findByText('Processing')).toBeInTheDocument();
  }, 10000);

  it('navigates to registry after stop and archive', async () => {
    renderAnalysis();

    const input = document.querySelector('input[type="file"]') as HTMLInputElement | null;
    const file = new File(['video'], 'sample.mp4', { type: 'video/mp4' });
    fireEvent.change(input as HTMLInputElement, { target: { files: [file] } });

    const stopButton = await screen.findByRole('button', { name: /stop and archive/i });
    fireEvent.click(stopButton);

    expect(await screen.findByText('Registry View')).toBeInTheDocument();
  }, 10000);
});
