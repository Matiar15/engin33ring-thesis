import { Play, Pause, Maximize, Loader2 } from 'lucide-react';
import { useVideoControls } from '@/features/analysis/hooks/useVideoControls.ts';
import { useBoundingBoxOverlay } from '@/features/analysis/hooks/useBoundingBoxOverlay.ts';
import { useVideoAnalysis } from '@/features/analysis/context';
import VideoPlayerProcessingIndicator from "@/features/analysis/components/VideoPlayerProcessingIndicator.tsx";

interface VideoPlayerProps {
  videoUrl: string;
  isProcessing: boolean;
}

const VideoPlayer = ({ videoUrl, isProcessing }: VideoPlayerProps) => {
  const { state, videoRef, pause, resume, finish } = useVideoAnalysis();
  const { isFinished } = state;

  const {
    containerRef,
    isPlaying,
    isPendingPlay,
    progress,
    currentTime,
    duration,
    togglePlay,
    toggleFullscreen,
  } = useVideoControls({
    autoPlay: isProcessing,
    onPlay: resume,
    onPause: pause,
    externalVideoRef: videoRef,
  });

  const { canvasRef } = useBoundingBoxOverlay({
    boxes: state.boundingBoxes,
    containerRef,
    isPaused: !isPlaying,
  });
  return (
    <div 
      ref={containerRef}
      className={`relative w-full aspect-video bg-black rounded-xl overflow-hidden neon-border group ${isFinished ? 'grayscale' : ''}`}
    >
      <video
        ref={videoRef}
        src={videoUrl}
        className="w-full h-full object-contain"
        muted
        preload="metadata"
        playsInline
        onEnded={finish}
      />
      
      {/* Canvas overlay for bounding boxes */}
      <canvas
        ref={canvasRef}
        className="absolute inset-0 pointer-events-none"
      />

      {isFinished && (
        <div className="absolute inset-0 bg-black/40 flex items-center justify-center z-10 pointer-events-none">
          <span className="text-white text-xl font-bold bg-black/60 px-6 py-3 rounded-lg border border-white/20">
            Video Analysis Complete!
          </span>
        </div>
      )}

      <VideoPlayerProcessingIndicator isProcessing={isProcessing} />

      {/* Controls */}
      <div className={`absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-black/80 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 ${isFinished ? 'pointer-events-none' : ''}`}>
        {/* Progress bar */}
        <div
          className={`h-1 bg-muted rounded-full mb-3 overflow-hidden 'cursor-not-allowed opacity-60'`}
          aria-disabled
        >
          <div
            className="h-full bg-primary transition-all duration-100"
            style={{ width: `${progress}%` }}
          />
        </div>

        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button
              onClick={togglePlay}
              disabled={isFinished || isPendingPlay}
              className="p-2 rounded-lg bg-primary/20 hover:bg-primary/30 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isPendingPlay ? (
                <Loader2 className="w-5 h-5 text-primary animate-spin" />
              ) : isPlaying ? (
                <Pause className="w-5 h-5 text-primary" />
              ) : (
                <Play className="w-5 h-5 text-primary" />
              )}
            </button>
            <span className="text-sm text-muted-foreground font-mono">
              {currentTime} / {duration}
            </span>
          </div>

          <button
            onClick={toggleFullscreen}
            disabled={isFinished}
            className="p-2 rounded-lg bg-muted/50 hover:bg-muted transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Maximize className="w-5 h-5 text-foreground" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default VideoPlayer;
