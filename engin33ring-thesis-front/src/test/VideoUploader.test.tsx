import { render, screen, fireEvent } from '@testing-library/react';
import { vi, describe, it, expect, beforeEach } from 'vitest';
import { useFileDrop } from '@/features/analysis/hooks/useFileDrop';
import VideoUploader from '@/features/analysis/components/VideoUploader';

vi.mock('@/features/analysis/hooks/useFileDrop', () => ({
  useFileDrop: vi.fn(),
}));

const mockedUseFileDrop = vi.mocked(useFileDrop);

describe('VideoUploader', () => {
  beforeEach(() => {
    mockedUseFileDrop.mockReset();
  });

  it('renders the upload heading and helper text', () => {
    mockedUseFileDrop.mockReturnValue({
      isDragging: false,
      error: null,
      dragProps: {
        onDragEnter: undefined,
        onDragLeave: undefined,
        onDragOver: undefined,
        onDrop: undefined
      },
      handleFileInput: vi.fn(),
    });

    render(<VideoUploader onVideoSelect={vi.fn()} />);

    expect(screen.getByText('Upload Video for Analysis')).toBeInTheDocument();
    expect(screen.getByText('Supports MP4, WebM, MOV')).toBeInTheDocument();
  });

  it('shows validation error when hook returns error', () => {
    mockedUseFileDrop.mockReturnValue({
      isDragging: false,
      error: 'Test error',
      dragProps: {
        onDragEnter: undefined,
        onDragLeave: undefined,
        onDragOver: undefined,
        onDrop: undefined
      },
      handleFileInput: vi.fn(),
    });

    render(<VideoUploader onVideoSelect={vi.fn()} />);

    expect(screen.getByText('Test error')).toBeInTheDocument();
  });

  it('wires file input change to handleFileInput', () => {
    const handleFileInput = vi.fn();
    mockedUseFileDrop.mockReturnValue({
      isDragging: false,
      error: null,
      dragProps: {
        onDragEnter: undefined,
        onDragLeave: undefined,
        onDragOver: undefined,
        onDrop: undefined
      },
      handleFileInput,
    });

    const { container } = render(<VideoUploader onVideoSelect={vi.fn()} />);

    const input = container.querySelector('input[type="file"]') as HTMLInputElement | null;
    expect(input).not.toBeNull();
    const file = new File(['video'], 'video.mp4', { type: 'video/mp4' });
    fireEvent.change(input as HTMLInputElement, { target: { files: [file] } });

    expect(handleFileInput).toHaveBeenCalledTimes(1);
  });
});
