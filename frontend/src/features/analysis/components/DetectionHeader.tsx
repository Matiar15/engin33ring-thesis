import {Activity} from "lucide-react";

interface DetectionHeaderProps {
    isProcessing: boolean;
    signsLength: number;
}

const DetectionHeader = ({isProcessing, signsLength } : DetectionHeaderProps) => {
  return (
    <div className="p-4 border-b border-border">
        <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
                <Activity className={`w-5 h-5 ${isProcessing ? 'text-neon-green animate-pulse' : 'text-muted-foreground'}`} />
                <h3 className="font-display font-semibold text-lg tracking-wide">Detection Log</h3>
            </div>
            <span className="text-sm text-muted-foreground font-mono">
            {signsLength} signs
          </span>
        </div>
    </div>
  );
}

export default DetectionHeader;