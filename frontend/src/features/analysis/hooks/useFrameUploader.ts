import { useEffect, useRef } from 'react';
import { frameService, FrameResponse } from '@/services/frameService';

interface UseFrameUploaderProps {
  isProcessing: boolean;
  videoFile: File | null;
  videoUrl: string | null;
  analysisId: string | null;
  userId: string | null;
  onFrameUploaded?: (data: FrameResponse) => void;
}

export function useFrameUploader({
  isProcessing,
  videoFile,
  videoUrl,
  analysisId,
  userId,
  onFrameUploaded,
}: UseFrameUploaderProps) {
  const frameCounter = useRef<number>(0);
  const frameUploadInterval = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    if (!isProcessing || !videoFile || !analysisId || !userId) {
      if (frameUploadInterval.current) {
        clearInterval(frameUploadInterval.current);
        frameUploadInterval.current = null;
      }
      return;
    }

    const canvas = document.createElement('canvas');
    const video = document.createElement('video');
    video.src = videoUrl || '';
    video.muted = true;

    const captureAndUploadFrame = async () => {
      try {
        if (video.paused || video.ended) return;

        canvas.width = video.videoWidth || 640;
        canvas.height = video.videoHeight || 480;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        canvas.toBlob(async (blob) => {
          if (!blob) return;

          const frameFile = new File(
            [blob],
            `frame_${frameCounter.current}.jpg`,
            { type: 'image/jpeg' }
          );

          try {
            const response = await frameService.uploadFrame(
              userId,
              analysisId,
              frameFile,
              frameCounter.current.toString(),
            );
            if (onFrameUploaded) {
              onFrameUploaded(response);
            }
            frameCounter.current++;
          } catch (error) {
            console.error('Failed to upload frame:', error);
          }
        }, 'image/jpeg', 0.8);
      } catch (error) {
        console.error('Failed to capture frame:', error);
      }
    };

    video.addEventListener('loadedmetadata', () => {
      video.play().catch(console.error);
      frameUploadInterval.current = setInterval(captureAndUploadFrame, 1000); // 1 frame per second
    });

    return () => {
      video.pause();
      video.src = '';
      if (frameUploadInterval.current) {
        clearInterval(frameUploadInterval.current);
      }
    };
  }, [isProcessing, videoFile, videoUrl, analysisId, userId]);

  const resetFrameCounter = () => {
    frameCounter.current = 0;
  };

  return { resetFrameCounter };
}

