import { useRef, useEffect, useState, useCallback, RefObject } from 'react';

interface UseVideoControlsOptions {
  autoPlay?: boolean;
  onPlay?: () => void;
  onPause?: () => void;
  externalVideoRef?: RefObject<HTMLVideoElement | null>;
}

export function useVideoControls({ autoPlay = false, onPlay, onPause, externalVideoRef }: UseVideoControlsOptions = {}) {
  const internalVideoRef = useRef<HTMLVideoElement>(null);
  const videoRef = externalVideoRef || internalVideoRef;
  const containerRef = useRef<HTMLDivElement>(null);

  const [isPlaying, setIsPlaying] = useState(false);
  const [isMuted, setIsMuted] = useState(true);
  const [isPendingPlay, setIsPendingPlay] = useState(false);
  const [progress, setProgress] = useState(0);
  const [currentTime, setCurrentTime] = useState('0:00');
  const [duration, setDuration] = useState('0:00');

  const formatTime = useCallback((seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  }, []);

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    const handleTimeUpdate = () => {
      setProgress((video.currentTime / video.duration) * 100);
      setCurrentTime(formatTime(video.currentTime));
    };

    const handleLoadedMetadata = () => {
      setDuration(formatTime(video.duration));
    };

    const handlePlay = () => {
      setIsPlaying(true);
      onPlay?.();
    };
    const handlePause = () => {
      setIsPlaying(false);
      onPause?.();
    };

    video.addEventListener('timeupdate', handleTimeUpdate);
    video.addEventListener('loadedmetadata', handleLoadedMetadata);
    video.addEventListener('play', handlePlay);
    video.addEventListener('pause', handlePause);

    return () => {
      video.removeEventListener('timeupdate', handleTimeUpdate);
      video.removeEventListener('loadedmetadata', handleLoadedMetadata);
      video.removeEventListener('play', handlePlay);
      video.removeEventListener('pause', handlePause);
    };
  }, [formatTime, onPlay, onPause, videoRef]);

  useEffect(() => {
    if (autoPlay && videoRef.current) {
      videoRef.current.play();
    }
  }, [autoPlay, videoRef]);

  const togglePlay = useCallback(() => {
    if (!videoRef.current || isPendingPlay) return;
    if (isPlaying) {
      videoRef.current.pause();
      return;
    }

    setIsPendingPlay(true);
    const playPromise = videoRef.current.play();
    if (playPromise && typeof playPromise.then === 'function') {
      playPromise
        .catch(() => {
          // Ignore autoplay errors to avoid unhandled promise rejections.
        })
        .finally(() => {
          setIsPendingPlay(false);
        });
    } else {
      setIsPendingPlay(false);
    }
  }, [isPlaying, isPendingPlay, videoRef]);

  const toggleMute = useCallback(() => {
    if (!videoRef.current) return;
    videoRef.current.muted = !isMuted;
    setIsMuted(!isMuted);
  }, [isMuted, videoRef]);

  const toggleFullscreen = useCallback(() => {
    if (!containerRef.current) return;
    if (document.fullscreenElement) {
      document.exitFullscreen();
    } else {
      containerRef.current.requestFullscreen();
    }
  }, []);

  return {
    videoRef,
    containerRef,
    isPlaying,
    isPendingPlay,
    isMuted,
    progress,
    currentTime,
    duration,
    togglePlay,
    toggleMute,
    toggleFullscreen,
  };
}
