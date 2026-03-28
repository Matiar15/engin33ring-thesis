import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Calendar, Clock, Eye, Scan, ArrowLeft, FileVideo, Target } from 'lucide-react';
import { ArchiveEntry } from "@/features/analysis/types";
import { initialArchiveData } from '@/mockData.ts';

const RegistryPage = () => {
  const navigate = useNavigate();
  // TODO: Replace with API call to fetch user's analysis history
  // const { data: entries, isLoading } = useQuery({
  //   queryKey: ['analyses', userId],
  //   queryFn: () => analysisService.getAnalyses(userId)
  // });
  const [entries] = useState<ArchiveEntry[]>(initialArchiveData);

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
            <p className="font-display font-bold text-2xl text-primary">{entries.length}</p>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="flex-1 p-4 sm:p-6">
        {entries.length === 0 ? (
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
                className="group glass-panel rounded-xl overflow-hidden neon-border hover:border-primary/50 transition-all duration-300 hover:scale-[1.02] animate-scale-in"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                {/* Thumbnail */}
                <div className="relative aspect-video bg-muted overflow-hidden">
                  {entry.thumbnail.startsWith('blob:') ? (
                    <video
                      src={entry.thumbnail}
                      className="w-full h-full object-cover"
                      muted
                    />
                  ) : (
                    <img
                      src={entry.thumbnail}
                      alt="Session thumbnail"
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                    />
                  )}
                  
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
                <div className="p-4">
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-2 text-muted-foreground">
                      <Calendar className="w-4 h-4" />
                      <span className="text-sm">
                        {entry.date.toLocaleDateString('en-US', {
                          month: 'short',
                          day: 'numeric',
                          year: 'numeric',
                        })}
                      </span>
                    </div>
                    <span className="text-xs text-muted-foreground font-mono">
                      {entry.date.toLocaleTimeString('en-US', {
                        hour: '2-digit',
                        minute: '2-digit',
                      })}
                    </span>
                  </div>

                  {/* Stats */}
                  <div className="flex items-center justify-between p-3 bg-muted/30 rounded-lg">
                    <div className="flex items-center gap-2">
                      <Target className="w-5 h-5 text-neon-green" />
                      <span className="text-sm font-medium">Signs Detected</span>
                    </div>
                    <span className="text-2xl font-display font-bold text-neon-green">
                      {entry.signsDetected}
                    </span>
                  </div>

                  {/* Top detections preview */}
                  {entry.detections.length > 0 && (
                    <div className="mt-3 flex flex-wrap gap-1.5">
                      {[...new Set(entry.detections.map(d => d.signType))].slice(0, 3).map((sign: string, i: number) => (
                        <span
                          key={i}
                          className="px-2 py-0.5 text-xs bg-primary/10 text-primary rounded-full border border-primary/20"
                        >
                          {sign}
                        </span>
                      ))}
                      {[...new Set(entry.detections.map(d => d.signType))].length > 3 && (
                        <span className="px-2 py-0.5 text-xs bg-muted text-muted-foreground rounded-full">
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
    </div>
  );
};

export default RegistryPage;
