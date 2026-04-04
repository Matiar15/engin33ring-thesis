import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { useAnalysisLifecycle } from '@/features/analysis/hooks/useAnalysisLifecycle';
import { analysisService } from '@/services/analysisService';
import { toast } from 'sonner';

vi.mock('@/services/analysisService');
vi.mock('sonner');

describe('useAnalysisLifecycle', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should initialize with null analysisId', () => {
    const { result } = renderHook(() => useAnalysisLifecycle('user123'));

    expect(result.current.analysisId).toBeNull();
  });

  it('should start analysis successfully', async () => {
    const mockResponse = { id: 'analysis_123' };
    vi.mocked(analysisService.createAnalysis).mockResolvedValue(mockResponse);

    const { result } = renderHook(() => useAnalysisLifecycle('user123'));

    const analysisId = await result.current.startAnalysis();
    expect(analysisId).toBe('analysis_123');

    await waitFor(() => {
      expect(result.current.analysisId).toBe('analysis_123');
    });

    expect(analysisService.createAnalysis).toHaveBeenCalledWith('user123');
    expect(toast.success).toHaveBeenCalledWith('Analysis started successfully');
  });

  it('should not start analysis without userId', async () => {
    const { result } = renderHook(() => useAnalysisLifecycle(null));

    const analysisId = await result.current.startAnalysis();

    expect(analysisId).toBeNull();
    expect(toast.error).toHaveBeenCalledWith('Please log in first');
    expect(analysisService.createAnalysis).not.toHaveBeenCalled();
  });

  it('should handle start analysis error', async () => {
    vi.mocked(analysisService.createAnalysis).mockRejectedValue(
      new Error('Network error')
    );

    const { result } = renderHook(() => useAnalysisLifecycle('user123'));

    const analysisId = await result.current.startAnalysis();

    expect(analysisId).toBeNull();
    expect(toast.error).toHaveBeenCalledWith('Failed to start analysis');
  });

  it('should end analysis successfully', async () => {
    vi.mocked(analysisService.createAnalysis).mockResolvedValue({ id: 'analysis_123' });
    vi.mocked(analysisService.endAnalysis).mockResolvedValue(undefined);

    const { result } = renderHook(() => useAnalysisLifecycle('user123'));

    // Start analysis first
    await result.current.startAnalysis();

    await waitFor(() => {
      expect(result.current.analysisId).toBe('analysis_123');
    });

    // End analysis
    const success = await result.current.endAnalysis();

    expect(success).toBe(true);
    expect(analysisService.endAnalysis).toHaveBeenCalledWith('analysis_123', 'user123');
    expect(toast.success).toHaveBeenCalledWith('Analysis archived successfully');
  });

  it('should not end analysis without userId', async () => {
    const { result } = renderHook(() => useAnalysisLifecycle(null));

    const success = await result.current.endAnalysis();

    expect(success).toBe(false);
    expect(toast.error).toHaveBeenCalledWith('User not authenticated or no active analysis');
    expect(analysisService.endAnalysis).not.toHaveBeenCalled();
  });

  it('should not end analysis without active analysisId', async () => {
    const { result } = renderHook(() => useAnalysisLifecycle('user123'));

    const success = await result.current.endAnalysis();

    expect(success).toBe(false);
    expect(toast.error).toHaveBeenCalledWith('User not authenticated or no active analysis');
  });

  it('should handle end analysis error', async () => {
    vi.mocked(analysisService.createAnalysis).mockResolvedValue({ id: 'analysis_123' });
    vi.mocked(analysisService.endAnalysis).mockRejectedValue(new Error('Server error'));

    const { result } = renderHook(() => useAnalysisLifecycle('user123'));

    await result.current.startAnalysis();
    await waitFor(() => {
      expect(result.current.analysisId).toBe('analysis_123');
    });
    const success = await result.current.endAnalysis();

    expect(success).toBe(false);
    expect(toast.error).toHaveBeenCalledWith('Failed to archive analysis');
  });

  it('should reset analysisId', async () => {
    vi.mocked(analysisService.createAnalysis).mockResolvedValue({ id: 'analysis_123' });

    const { result } = renderHook(() => useAnalysisLifecycle('user123'));

    await result.current.startAnalysis();
    await waitFor(() => {
      expect(result.current.analysisId).toBe('analysis_123');
    });

    result.current.resetAnalysis();

    await waitFor(() => {
      expect(result.current.analysisId).toBeNull();
    });
  });
});

