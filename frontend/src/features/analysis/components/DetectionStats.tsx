interface DetectionStatsProps {
    stats: {
        count: number;
        avgConfidence: number;
    }
}

const DetectionStats = ({ stats } : DetectionStatsProps) => {
    return (<div className="p-4 border-b border-border grid grid-cols-2 gap-4">
        <div className="text-center p-3 bg-muted/30 rounded-lg">
            <p className="text-2xl font-display font-bold text-primary">{stats.count}</p>
            <p className="text-xs text-muted-foreground uppercase tracking-wide">Detected</p>
        </div>
        <div className="text-center p-3 bg-muted/30 rounded-lg">
            <p className="text-2xl font-display font-bold text-neon-green">
                {stats.avgConfidence}%
            </p>
            <p className="text-xs text-muted-foreground uppercase tracking-wide">Avg Conf</p>
        </div>
    </div>
    );
};

export default DetectionStats;