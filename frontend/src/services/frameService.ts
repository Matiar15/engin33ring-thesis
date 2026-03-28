import { apiClient } from './apiClient';

export interface FrameResponse {
  id: string;
  frame_url: string;
  created_at: string;
}

export interface FrameService {
  uploadFrame: (
    userId: string,
    analysisId: string,
    frameFile: File,
    incomingId: string
  ) => Promise<FrameResponse>;
}

export const frameService: FrameService = {
  uploadFrame: async (
    userId: string,
    analysisId: string,
    frameFile: File,
    incomingId: string
  ) => {
    const formData = new FormData();
    formData.append('user_id', userId);
    formData.append('analysis_id', analysisId);
    formData.append('frame', frameFile);
    formData.append('incoming_id', incomingId);

    return apiClient.postFormData<FrameResponse>('/frames/', formData);
  },
};

