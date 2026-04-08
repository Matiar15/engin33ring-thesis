import { apiClient } from './apiClient';

export interface CreateAnalysisResponse {
  id: string;
}

export interface AnalysisFrame {
  id: string;
  frame_url: string;
  created_at: string;
  sign?: string;
  x?: number;
  y?: number;
  width?: number;
  height?: number;
}

export interface Analysis {
  id: string;
  user_id: string;
  status: string;
  modified_at: string;
  frames?: AnalysisFrame[];
  video_url?: string;
}

export interface VideoUrlResponse {
  url: string;
}

export interface AnalysisService {
  createAnalysis: (userId: string) => Promise<CreateAnalysisResponse>;
  endAnalysis: (analysisId: string, userId: string) => Promise<void>;
  getAnalyses: (limit?: number, offset?: number) => Promise<Analysis[]>;
  getVideoUrl: (analysisId: string) => Promise<VideoUrlResponse>;
}

export const analysisService: AnalysisService = {
  createAnalysis: async (userId: string) => {
    return apiClient.post<CreateAnalysisResponse>('/analysis/', {
      user_id: userId,
    });
  },

  endAnalysis: async (analysisId: string, userId: string) => {
    return apiClient.patch<void>('/analysis/', {
      id: analysisId,
      user_id: userId,
    });
  },

  getAnalyses: async (limit = 10, offset = 0) => {
    return apiClient.get<Analysis[]>(`/analysis?limit=${limit}&offset=${offset}`);
  },

  getVideoUrl: async (analysisId: string) => {
    return apiClient.get<VideoUrlResponse>(`/analysis/${analysisId}/video-url`);
  },
};
