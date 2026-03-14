import DetectionLogList from "@/features/analysis/components/DetectionLogList.tsx";
import DetectionLogEmptyList from "@/features/analysis/components/DetectionLogEmptyList.tsx";

interface DetectionLogSectionProps {
    scrollRef: React.RefObject<HTMLDivElement>;
    logs: any[];
    isProcessing: boolean;
    reversedLogs: any[];
    getConfidenceLevel: (confidence: number) => 'high' | 'medium' | 'low';
}

const DetectionLogSection = ({
                                 scrollRef,
                                 logs,
                                 isProcessing,
                                 reversedLogs,
                                 getConfidenceLevel
                             }: DetectionLogSectionProps) => {
    const logList = logs.length === 0 ? (
        <DetectionLogEmptyList isProcessing={isProcessing}/>
    ) : (
        <DetectionLogList reversedLogs={reversedLogs} getConfidenceLevel={getConfidenceLevel}/>
    );

    return (
        <div ref={scrollRef} className="flex-1 overflow-y-auto p-2 space-y-2">
            {logList}
        </div>
    )
}

export default DetectionLogSection;