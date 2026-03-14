import { describe, it, expect } from 'vitest';
import { renderHook } from '@testing-library/react';
import { useDetectionStats } from '@/features/analysis/hooks/useDetectionStats';

const makeLog = (id: string, confidence: number) => ({
  id,
  timestamp: new Date('2025-01-01T10:00:00Z'),
  signType: 'Stop Sign',
  confidence,
});

describe('useDetectionStats', () => {
  it('calculates count and average confidence', () => {
    const logs = [makeLog('1', 90), makeLog('2', 100)];
    const { result } = renderHook(() => useDetectionStats(logs));

    expect(result.current.stats.count).toBe(2);
    expect(result.current.stats.avgConfidence).toBe(95);
  });

  it('returns 0 average for empty logs', () => {
    const { result } = renderHook(() => useDetectionStats([]));

    expect(result.current.stats.count).toBe(0);
    expect(result.current.stats.avgConfidence).toBe(0);
  });

  it('returns reversed logs without mutating original', () => {
    const logs = [makeLog('1', 80), makeLog('2', 85)];
    const { result } = renderHook(() => useDetectionStats(logs));

    expect(result.current.reversedLogs[0].id).toBe('2');
    expect(logs[0].id).toBe('1');
  });
});

