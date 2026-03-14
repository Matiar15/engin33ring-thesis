import { useEffect, useRef, useMemo } from 'react';
import { DetectionLog } from '@/features/analysis/types';

export function useDetectionStats(logs: DetectionLog[]) {
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new logs arrive
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [logs]);

  const stats = useMemo(() => ({
    count: logs.length,
    avgConfidence: logs.length > 0
      ? Math.round(logs.reduce((sum, log) => sum + log.confidence, 0) / logs.length)
      : 0,
  }), [logs]);

  const getConfidenceLevel = (confidence: number): 'high' | 'medium' | 'low' => {
    if (confidence >= 95) return 'high';
    if (confidence >= 85) return 'medium';
    return 'low';
  };

  // Logs in reverse order (newest first)
  const reversedLogs = useMemo(() => [...logs].reverse(), [logs]);

  return {
    scrollRef,
    stats,
    reversedLogs,
    getConfidenceLevel,
  };
}

