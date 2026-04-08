import { useEffect, useRef, RefObject } from 'react';
import { frameService, FrameResponse } from '@/services/frameService';

interface UseFrameUploaderProps {
  isProcessing: boolean;
  videoRef: RefObject<HTMLVideoElement | null>;
  analysisId: string | null;
  userId: string | null;
  onFrameUploaded?: (data: FrameResponse) => void;
}

export function useFrameUploader({
  isProcessing,
  videoRef,
  analysisId,
  userId,
  onFrameUploaded,
}: UseFrameUploaderProps) {
  const frameCounter = useRef<number>(0);
  const activeRef = useRef(false);

  useEffect(() => {
    if (!isProcessing || !analysisId || !userId) {
      activeRef.current = false;
      return;
    }

    activeRef.current = true;
    let intervalId: ReturnType<typeof setInterval> | null = null;

    const captureAndUpload = async () => {
      if (!activeRef.current) return;

      const video = videoRef.current;
      if (!video || video.paused || video.ended) return;
      if (!video.videoWidth || !video.videoHeight) return;

      // Fresh canvas every capture – avoids stale GL/2D context state
      // that causes garbled frames in Firefox macOS.
      const canvas = document.createElement('canvas');
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      const ctx = canvas.getContext('2d');
      if (!ctx) return;

      ctx.drawImage(video, 0, 0);

      const blob: Blob | null = await new Promise((resolve) =>
        canvas.toBlob(resolve, 'image/jpeg', 0.8),
      );
      if (!blob) return;

      const frameFile = new File(
        [blob],
        `frame_${frameCounter.current}.jpg`,
        { type: 'image/jpeg' },
      );

      try {
        const response = await frameService.uploadFrame(
          userId!,
          analysisId!,
          frameFile,
          frameCounter.current.toString(),
        );
        onFrameUploaded?.(response);
        frameCounter.current++;
      } catch (error) {
        console.error('Failed to upload frame:', error);
      }
    };

    // requestVideoFrameCallback fires only when a new decoded frame is
    // actually presented – the pixel data is guaranteed to be ready for
    // canvas readback (fixes Firefox macOS corruption).
    const video = videoRef.current;
    const supportsRVFC =
      video && 'requestVideoFrameCallback' in video;

    if (supportsRVFC) {
      let lastCaptureMs = 0;

      const onFrame = () => {
        if (!activeRef.current) return;

        const now = performance.now();
        if (now - lastCaptureMs >= 100) {
          lastCaptureMs = now;
          captureAndUpload().catch(console.error);
        }

        // Schedule next callback
        videoRef.current?.requestVideoFrameCallback(onFrame);
      };

      video.requestVideoFrameCallback(onFrame);
    } else {
      // Fallback for browsers without requestVideoFrameCallback
      intervalId = setInterval(() => {
        captureAndUpload().catch(console.error);
      }, 100);
    }

    return () => {
      activeRef.current = false;
      if (intervalId) clearInterval(intervalId);
    };
  }, [isProcessing, videoRef, analysisId, userId, onFrameUploaded]);

  const resetFrameCounter = () => {
    frameCounter.current = 0;
  };

  return { resetFrameCounter };
}