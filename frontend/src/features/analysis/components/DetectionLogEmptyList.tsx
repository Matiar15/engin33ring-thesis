import {Clock} from "lucide-react";

interface DetectionLogEmptyListProps {
    isProcessing: boolean;
}

const DetectionLogEmptyList = ({isProcessing} : DetectionLogEmptyListProps) => {
    return (<div className="flex flex-col items-center justify-center h-full text-center p-4">
        <Clock className="w-10 h-10 text-muted-foreground/50 mb-3"/>
        <p className="text-muted-foreground text-sm">
            {isProcessing ? 'Waiting for detections...' : 'Start processing to see detections'}
        </p>
    </div>)
}

export default DetectionLogEmptyList;