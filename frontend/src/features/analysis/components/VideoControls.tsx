import { Square, Loader2 } from "lucide-react";

interface VideoControlsProps {
    isProcessing: boolean;
    isFinished: boolean;
    isSaving: boolean;
    videoFile: File | null;
    stopAndArchive: () => void;
    reset: () => void;
}

const VideoControls = ({ isProcessing, isFinished, isSaving, videoFile, stopAndArchive, reset} : VideoControlsProps) => {
    return (
        <div className="flex items-center justify-between gap-4">
            <div className="flex items-center gap-4">
                <div className="flex items-center gap-2 px-3 py-2 bg-muted/50 rounded-lg">
                    <div className={`w-2 h-2 rounded-full ${
                        isSaving ? 'bg-yellow-400 animate-pulse' :
                        isProcessing ? 'bg-neon-green animate-pulse' :
                        isFinished ? 'bg-blue-500' :
                        'bg-muted-foreground'
                    }`} />
                    <span className="text-sm font-medium">
                      {isSaving ? 'Saving...' : isProcessing ? 'Processing' : isFinished ? 'Finished' : 'Paused'}
                    </span>
                </div>
                {videoFile && (
                    <span className="text-sm text-muted-foreground truncate max-w-xs">
                      {videoFile.name}
                    </span>
                )}
            </div>

            <div className="flex items-center gap-3">
                <button
                    onClick={reset}
                    disabled={isSaving}
                    className="px-4 py-2 bg-muted hover:bg-muted/80 rounded-lg font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    New Video
                </button>

                <button
                    onClick={stopAndArchive}
                    disabled={isSaving}
                    aria-label="Stop and Archive"
                    className="flex items-center gap-2 px-3 py-3 sm:px-6 bg-destructive hover:bg-destructive/90 text-destructive-foreground rounded-lg font-display font-bold uppercase tracking-wider transition-all shadow-lg hover:shadow-destructive/25 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:shadow-none"
                    style={!isSaving ? {
                        boxShadow: '0 0 20px hsl(0 84% 60% / 0.4), 0 0 40px hsl(0 84% 60% / 0.2)'
                    } : {}}
                >
                    {isSaving
                        ? <Loader2 className="w-4 h-4 animate-spin" />
                        : <Square className="w-4 h-4 fill-current" />
                    }
                    <span className="hidden sm:inline">{isSaving ? 'Saving...' : 'Stop & Archive'}</span>
                </button>
            </div>
        </div>
    );
};


export default VideoControls;