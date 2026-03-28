import { useState, useCallback } from 'react';
import { analysisService } from '@/services/analysisService';
import { toast } from 'sonner';

export function useAnalysisLifecycle(userId: string | null) {
  const [analysisId, setAnalysisId] = useState<string | null>(null);

  const startAnalysis = useCallback(async () => {
    if (!userId) {
      toast.error('Please log in first');
      return null;
    }

    try {
      const response = await analysisService.createAnalysis(userId);
      setAnalysisId(response.id);
      toast.success('Analysis started successfully');
      return response.id;
    } catch (error) {
      console.error('Failed to create analysis:', error);
      toast.error('Failed to start analysis');
      return null;
    }
  }, [userId]);

  const endAnalysis = useCallback(async () => {
    if (!userId || !analysisId) {
      toast.error('User not authenticated or no active analysis');
      return false;
    }

    try {
      await analysisService.endAnalysis(analysisId, userId);
      toast.success('Analysis archived successfully');
      return true;
    } catch (error) {
      console.error('Failed to end analysis:', error);
      toast.error('Failed to archive analysis');
      return false;
    }
  }, [analysisId, userId]);

  const resetAnalysis = useCallback(() => {
    setAnalysisId(null);
  }, []);

  return {
    analysisId,
    startAnalysis,
    endAnalysis,
    resetAnalysis,
  };
}

