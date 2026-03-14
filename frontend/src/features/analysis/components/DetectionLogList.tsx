import {AlertTriangle, CircleCheck, Zap} from "lucide-react";
import {DetectionLog} from "@/features/analysis/types";

interface DetectionLogListProps {
    reversedLogs: DetectionLog[];
    getConfidenceLevel: (confidence: number) => 'high' | 'medium' | 'low';
}

const CONFIDENCE_STYLES = {
    high: { color: 'text-neon-green', Icon: CircleCheck },
    medium: { color: 'text-primary', Icon: Zap },
    low: { color: 'text-neon-yellow', Icon: AlertTriangle },
} as const;

const DetectionLogList = ({ reversedLogs, getConfidenceLevel }: DetectionLogListProps) => {
    return (
            reversedLogs.map((log, index) => {
                const level = getConfidenceLevel(log.confidence);
                const { color, Icon } = CONFIDENCE_STYLES[level];

                return (
                    <div
                        key={log.id}
                        className={`p-3 rounded-lg bg-muted/30 border border-border/50 transition-all duration-300 ${
                            index === 0 ? 'animate-slide-in-right border-primary/30' : ''
                        }`}
                    >
                        <div className="flex items-start justify-between gap-2">
                            <div className="flex items-center gap-2">
                                <Icon className={`w-4 h-4 ${color}`} />
                                <span className="font-medium text-sm">{log.signType}</span>
                            </div>
                            <span className={`text-sm font-mono font-semibold ${color}`}>
                    {log.confidence}%
                  </span>
                        </div>
                        <p className="text-xs text-muted-foreground mt-1 font-mono">
                            {log.timestamp.toLocaleTimeString()} </p>
                    </div>
                );
            })
    )
}

export default DetectionLogList;