import { Play, Pause, Volume2, VolumeX, Maximize } from 'lucide-react';
import { useVideoControls } from '@/features/analysis/hooks/useVideoControls';
import { useBoundingBoxOverlay } from '@/features/analysis/hooks/useBoundingBoxOverlay';
import { useVideoAnalysis } from '@/features/analysis/context';
import VideoPlayerProcessingIndicator from "@/features/analysis/components/VideoPlayerProcessingIndicator.tsx";

interface VideoPlayerProps {
  videoUrl: string;
  isProcessing: boolean;
}

const VideoPlayer = ({ videoUrl, isProcessing }: VideoPlayerProps) => {
  const { state, pause, resume } = useVideoAnalysis();

  const {
    videoRef,
    containerRef,
    isPlaying,
    isMuted,
    progress,
    currentTime,
    duration,
    togglePlay,
    toggleMute,
    toggleFullscreen,
  } = useVideoControls({
    autoPlay: isProcessing,
    onPlay: resume,
    onPause: pause,
  });

  const { canvasRef } = useBoundingBoxOverlay({
    boxes: state.boundingBoxes,
    containerRef,
  });
  return (
    <div 
      ref={containerRef}
      className="relative w-full aspect-video bg-black rounded-xl overflow-hidden neon-border group"
    >
      <video
        ref={videoRef}
        src={videoUrl}
        className="w-full h-full object-contain"
        muted={isMuted}
        loop
        preload="metadata"
        playsInline
      />
      
      {/* Canvas overlay for bounding boxes */}
      <canvas
        ref={canvasRef}
        className="absolute inset-0 pointer-events-none"
      />

      <VideoPlayerProcessingIndicator isProcessing={isProcessing} />

      {/* Controls */}
      <div className="absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-black/80 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300">
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
              className="p-2 rounded-lg bg-primary/20 hover:bg-primary/30 transition-colors"
            >
              {isPlaying ? (
                <Pause className="w-5 h-5 text-primary" />
              ) : (
                <Play className="w-5 h-5 text-primary" />
              )}
            </button>
            <button
              onClick={toggleMute}
              className="p-2 rounded-lg bg-muted/50 hover:bg-muted transition-colors"
            >
              {isMuted ? (
                <VolumeX className="w-5 h-5 text-muted-foreground" />
              ) : (
                <Volume2 className="w-5 h-5 text-foreground" />
              )}
            </button>
            <span className="text-sm text-muted-foreground font-mono">
              {currentTime} / {duration}
            </span>
          </div>

          <button
            onClick={toggleFullscreen}
            className="p-2 rounded-lg bg-muted/50 hover:bg-muted transition-colors"
          >
            <Maximize className="w-5 h-5 text-foreground" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default VideoPlayer;
