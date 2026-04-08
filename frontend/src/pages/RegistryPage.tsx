import { useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { Calendar, Clock, Eye, Scan, ArrowLeft, FileVideo, Target, Loader2, X } from 'lucide-react';
import { ArchiveEntry } from "@/features/analysis/types";
import { analysisService } from '@/services/analysisService';
import { useState } from 'react';

const RegistryPage = () => {
  const navigate = useNavigate();
  const [playingVideo, setPlayingVideo] = useState<string | null>(null);
  
  const { data: analyses, isLoading } = useQuery({
    queryKey: ['analyses'],
    queryFn: () => analysisService.getAnalyses(50, 0)
  });

  const handleOpenVideo = async (analysisId: string) => {
    try {
      const { url } = await analysisService.getVideoUrl(analysisId);
      setPlayingVideo(url);
    } catch (e) {
      console.error(e);
    }
  };

  const entries: ArchiveEntry[] = (analyses || []).map(a => {
    const signsCount = a.frames?.filter(f => f.sign).length || 0;
    const durationMins = Math.floor((a.frames?.length || 0) / 60);
    const durationSecs = (a.frames?.length || 0) % 60;
    
    return {
      id: a.id || (a as any)._id,
      thumbnail: '', // We don't have an easily accessible thumbnail
      date: new Date(a.modified_at),
      duration: `${durationMins}:${durationSecs.toString().padStart(2, '0')}`,
      signsDetected: signsCount,
      detections: (a.frames || []).filter(f => f.sign).map((f, i) => ({
        id: f.id || String(i),
        timestamp: new Date(f.created_at),
        signType: f.sign!,
        confidence: 100 // Backend model frame doesn't return confidence atm
      }))
    };
  });

  return (
    <div className="min-h-screen flex flex-col animate-fade-in">
      {/* Header */}
      <header className="flex flex-col gap-4 px-4 py-4 border-b border-border bg-card/50 backdrop-blur-sm sm:flex-row sm:items-center sm:justify-between sm:px-6">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:gap-4">
          <button
            onClick={() => navigate('/analysis')}
            className="w-fit p-2 rounded-lg bg-muted hover:bg-muted/80 transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-primary/10 neon-border">
              <Scan className="w-6 h-6 text-primary" />
            </div>
            <div>
              <h1 className="font-display font-bold text-xl tracking-wider text-primary neon-text">
                ARCHIVE
              </h1>
              <p className="text-xs text-muted-foreground">Analysis History</p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-4 sm:justify-end">
          <div className="text-left sm:text-right">
            <p className="text-sm text-muted-foreground">Total Sessions</p>
            <p className="font-display font-bold text-2xl text-primary">{isLoading ? '-' : entries.length}</p>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="flex-1 p-4 sm:p-6">
        {isLoading ? (
          <div className="flex items-center justify-center h-full">
            <Loader2 className="w-8 h-8 animate-spin text-primary" />
          </div>
        ) : entries.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center px-4">
            <div className="p-6 rounded-full bg-muted/30 mb-6">
              <FileVideo className="w-16 h-16 text-muted-foreground/50" />
            </div>
            <h2 className="text-xl font-display font-semibold mb-2">No Archived Sessions</h2>
            <p className="text-muted-foreground max-w-md">
              Process and archive a video analysis to see it here.
            </p>
            <button
              onClick={() => navigate('/analysis')}
              className="mt-6 px-6 py-3 bg-primary text-primary-foreground font-display font-bold uppercase tracking-wider rounded-lg hover:bg-primary/90 transition-colors"
            >
              Start Analysis
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 sm:gap-6 xl:grid-cols-3">
            {entries.map((entry, index) => (
              <div
                key={entry.id}
                onClick={() => handleOpenVideo(entry.id)}
                className="group glass-panel rounded-xl overflow-hidden neon-border hover:border-primary/50 transition-all duration-300 hover:scale-[1.02] cursor-pointer animate-scale-in"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                {/* Thumbnail */}
                <div className="relative aspect-video bg-muted overflow-hidden flex items-center justify-center">
                  <FileVideo className="w-12 h-12 text-muted-foreground/30" />
                  
                  {/* Overlay gradient */}
                  <div className="absolute inset-0 bg-gradient-to-t from-background/80 via-transparent to-transparent" />
                  
                  {/* Duration badge */}
                  <div className="absolute top-3 right-3 flex items-center gap-1.5 px-2 py-1 bg-background/80 backdrop-blur-sm rounded-lg">
                    <Clock className="w-3.5 h-3.5 text-primary" />
                    <span className="text-xs font-mono font-medium">{entry.duration}</span>
                  </div>

                  {/* Play overlay */}
                  <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                    <div className="p-4 rounded-full bg-primary/20 backdrop-blur-sm border border-primary/30">
                      <Eye className="w-8 h-8 text-primary" />
                    </div>
                  </div>
                </div>

                {/* Info */}
                <div className="p-4 flex flex-col gap-3">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2 text-muted-foreground">
                      <Calendar className="w-4 h-4" />
                      <span className="text-sm font-medium">
                        {entry.date.toLocaleDateString('en-US', {
                          month: 'short',
                          day: 'numeric',
                          year: 'numeric',
                        })}
                      </span>
                    </div>
                    <span className="text-xs text-muted-foreground font-mono bg-muted/50 px-2 py-1 rounded-md">
                      {entry.date.toLocaleTimeString('en-US', {
                        hour: '2-digit',
                        minute: '2-digit',
                      })}
                    </span>
                  </div>

                  {/* Stats */}
                  <div className="flex items-center justify-between p-3 bg-muted/20 border border-border/50 rounded-lg">
                    <div className="flex items-center gap-2">
                      <Target className="w-4 h-4 text-neon-green" />
                      <span className="text-sm font-medium text-muted-foreground">Total Detections</span>
                    </div>
                    <span className="text-xl font-display font-bold text-neon-green">
                      {entry.signsDetected}
                    </span>
                  </div>

                  {/* Top detections preview */}
                  {entry.detections.length > 0 && (
                    <div className="flex flex-wrap gap-1.5 pt-1">
                      {[...new Set(entry.detections.map(d => d.signType))].slice(0, 3).map((sign: string, i: number) => (
                        <span
                          key={i}
                          className="px-2 py-1 text-[10px] font-medium tracking-wide bg-primary/10 text-primary rounded-full border border-primary/20 uppercase"
                        >
                          {sign}
                        </span>
                      ))}
                      {[...new Set(entry.detections.map(d => d.signType))].length > 3 && (
                        <span className="px-2 py-1 text-[10px] font-medium tracking-wide bg-muted text-muted-foreground rounded-full border border-border/50 uppercase">
                          +{[...new Set(entry.detections.map(d => d.signType))].length - 3} more
                        </span>
                      )}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </main>

      {/* Video Modal */}
      {playingVideo && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/90 p-4 sm:p-8 animate-fade-in">
          <button
            onClick={() => setPlayingVideo(null)}
            className="absolute top-4 right-4 p-2 rounded-full bg-white/10 hover:bg-white/20 transition-colors text-white"
          >
            <X className="w-6 h-6" />
          </button>
          <div className="w-full max-w-5xl rounded-xl overflow-hidden bg-black shadow-2xl ring-1 ring-white/10">
            <video
              src={playingVideo}
              controls
              autoPlay
              className="w-full max-h-[85vh] object-contain"
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default RegistryPage;
