import { describe, it, expect, vi, beforeEach } from 'vitest';
import { frameService } from '@/services/frameService';
import { apiClient } from '@/services/apiClient';

vi.mock('@/services/apiClient', () => ({
  apiClient: {
    postFormData: vi.fn(),
  },
}));

describe('frameService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('uploadFrame', () => {
    it('should upload frame with correct FormData', async () => {
      const mockResponse = {
        sign: 'speed_limit_30',
        bounding_box: {
          x: 10,
          y: 20,
          width: 50,
          height: 60,
        },
      };
      vi.mocked(apiClient.postFormData).mockResolvedValue(mockResponse);

      const mockFile = new File(['image data'], 'test.jpg', { type: 'image/jpeg' });
      const userId = 'user_123';
      const analysisId = 'analysis_456';
      const incomingId = 'frame_0';

      const result = await frameService.uploadFrame(
        userId,
        analysisId,
        mockFile,
        incomingId
      );

      expect(result).toEqual(mockResponse);
      expect(apiClient.postFormData).toHaveBeenCalledWith(
        '/frames/',
        expect.any(FormData)
      );

      // Verify FormData contents
      const callArgs = vi.mocked(apiClient.postFormData).mock.calls[0];
      const formData = callArgs[1] as FormData;

      expect(formData.get('user_id')).toBe(userId);
      expect(formData.get('analysis_id')).toBe(analysisId);
      expect(formData.get('incoming_id')).toBe(incomingId);
      expect(formData.get('frame')).toBe(mockFile);
    });

    it('should handle upload errors', async () => {
      vi.mocked(apiClient.postFormData).mockRejectedValue(
        new Error('Upload failed')
      );

      const mockFile = new File(['data'], 'test.jpg', { type: 'image/jpeg' });

      await expect(
        frameService.uploadFrame('user_123', 'analysis_456', mockFile, 'frame_0')
      ).rejects.toThrow('Upload failed');
    });

    it('should handle different file types', async () => {
      const mockResponse = {
        id: 'frame_002',
        frame_url: 'http://storage.com/frame.png',
        created_at: '2026-03-15T10:01:00Z',
      };
      vi.mocked(apiClient.postFormData).mockResolvedValue(mockResponse);

      const mockFile = new File(['image data'], 'test.png', { type: 'image/png' });

      const result = await frameService.uploadFrame(
        'user_789',
        'analysis_999',
        mockFile,
        'frame_5'
      );

      expect(result).toEqual(mockResponse);
      const callArgs = vi.mocked(apiClient.postFormData).mock.calls[0];
      const formData = callArgs[1] as FormData;
      expect(formData.get('frame')).toBe(mockFile);
    });
  });
});

