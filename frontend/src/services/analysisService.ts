import { apiClient } from './apiClient';

export interface CreateAnalysisResponse {
  id: string;
}

export interface AnalysisService {
  createAnalysis: (userId: string) => Promise<CreateAnalysisResponse>;
  endAnalysis: (analysisId: string, userId: string) => Promise<void>;
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
};

