const DetectionProcessingIndicator = ({isProcessing}) => {
    return (
        <div className="p-4 border-t border-border">
            <div className="flex items-center gap-3">
                <div className="relative">
                    <div className={`w-3 h-3 rounded-full ${isProcessing ? 'bg-neon-green' : 'bg-muted-foreground'}`}/>
                    {isProcessing && (
                        <div className="absolute inset-0 w-3 h-3 bg-neon-green rounded-full animate-ping"/>
                    )}
                </div>

                {isProcessing ?
                    (
                        <span className="text-sm text-neon-green font-display uppercase tracking-wider">
                        Live Analysis Active
                    </span>
                    ) : (
                        <span className="text-sm text-muted-foreground font-display uppercase tracking-wider">
                        Analysis Paused
                    </span>
                    )
                }
            </div>
        </div>
    );
}

export default DetectionProcessingIndicator;