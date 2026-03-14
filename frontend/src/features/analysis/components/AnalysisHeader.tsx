import { useNavigate } from 'react-router-dom';
import { Scan, Archive, LogOut } from 'lucide-react';

export function AnalysisHeader() {
  const navigate = useNavigate();

  return (
    <header className="flex flex-col gap-4 px-4 py-4 border-b border-border bg-card/50 backdrop-blur-sm sm:flex-row sm:items-center sm:justify-between sm:px-6">
      <div className="flex items-center gap-3">
        <div className="p-2 rounded-lg bg-primary/10 neon-border">
          <Scan className="w-6 h-6 text-primary" />
        </div>
        <div>
          <h1 className="font-display font-bold text-xl tracking-wider text-primary neon-text">
            MS TRAFFIC SIGN ANALYZER
          </h1>
          <p className="text-xs text-muted-foreground">Traffic Sign Recognition System</p>
        </div>
      </div>

      <div className="flex flex-wrap items-center gap-3 sm:flex-nowrap sm:justify-end">
        <button
          onClick={() => navigate('/registry')}
          className="flex items-center gap-2 px-4 py-2 bg-secondary hover:bg-secondary/80 rounded-lg transition-colors"
        >
          <Archive className="w-4 h-4" />
          <span className="font-medium">Archive</span>
        </button>
        <button
          onClick={() => navigate('/')}
          className="flex items-center gap-2 px-4 py-2 text-muted-foreground hover:text-foreground hover:bg-muted rounded-lg transition-colors"
        >
          <LogOut className="w-4 h-4" />
          <span className="font-medium">Logout</span>
        </button>
      </div>
    </header>
  );
}
