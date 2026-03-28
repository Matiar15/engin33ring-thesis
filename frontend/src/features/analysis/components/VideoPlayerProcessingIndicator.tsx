const VideoPlayerProcessingIndicator = ({isProcessing}) => {
    const color = isProcessing ? 'neon-green' : 'muted-foreground';
    return (<div
        data-testid="video-processing-indicator"
        className={`absolute top-4 left-4 flex items-center gap-2 px-3 py-1.5 bg-${color}/20 border bg-${color}/50 rounded-full animate-pulse`}>
        <div className={`w-2 h-2 rounded-full bg-${color}`}/>
        <span className={`text-${color} text-sm font-display uppercase tracking-wider`}>
       {isProcessing ? 'Processing...' : 'Paused'} </span>
    </div>);
}

export default VideoPlayerProcessingIndicator;