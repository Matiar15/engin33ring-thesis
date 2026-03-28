import { describe, it, expect, vi, beforeEach } from 'vitest';
import { analysisService } from '@/services/analysisService';
import { apiClient } from '@/services/apiClient';

vi.mock('@/services/apiClient', () => ({
  apiClient: {
    post: vi.fn(),
    patch: vi.fn(),
  },
}));

describe('analysisService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('createAnalysis', () => {
    it('should call API with correct parameters', async () => {
      const mockResponse = { id: 'analysis_456' };
      vi.mocked(apiClient.post).mockResolvedValue(mockResponse);

      const result = await analysisService.createAnalysis('user_123');

      expect(result).toEqual(mockResponse);
      expect(apiClient.post).toHaveBeenCalledWith('/analysis/', {
        user_id: 'user_123',
      });
    });

    it('should throw error when API fails', async () => {
      vi.mocked(apiClient.post).mockRejectedValue(new Error('Network error'));

      await expect(analysisService.createAnalysis('user_123')).rejects.toThrow(
        'Network error'
      );
    });
  });

  describe('endAnalysis', () => {
    it('should call API with correct parameters', async () => {
      vi.mocked(apiClient.patch).mockResolvedValue(undefined);

      await analysisService.endAnalysis('analysis_789', 'user_123');

      expect(apiClient.patch).toHaveBeenCalledWith('/analysis/', {
        id: 'analysis_789',
        user_id: 'user_123',
      });
    });

    it('should handle API errors', async () => {
      vi.mocked(apiClient.patch).mockRejectedValue(new Error('Server error'));

      await expect(
        analysisService.endAnalysis('analysis_789', 'user_123')
      ).rejects.toThrow('Server error');
    });
  });
});

