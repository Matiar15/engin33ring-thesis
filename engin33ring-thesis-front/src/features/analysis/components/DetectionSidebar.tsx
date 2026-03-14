import {DetectionLog} from "@/features/analysis/types";
import {useDetectionStats} from '@/features/analysis/hooks/useDetectionStats';
import DetectionHeader from "@/features/analysis/components/DetectionHeader.tsx";
import DetectionStats from "@/features/analysis/components/DetectionStats.tsx";
import DetectionLogSection from "@/features/analysis/components/DetectionLogSection.tsx";

interface DetectionSidebarProps {
    logs: DetectionLog[];
    isProcessing: boolean;
}

const DetectionSidebar = ({logs, isProcessing}: DetectionSidebarProps) => {
    const {scrollRef, stats, reversedLogs, getConfidenceLevel} = useDetectionStats(logs);

    return (
        <div className="h-full flex flex-col bg-card rounded-xl neon-border overflow-hidden">
            <DetectionHeader
                isProcessing={isProcessing}
                signsLength={logs.length}
            />
            <DetectionStats stats={stats}/>
            <DetectionLogSection
                scrollRef={scrollRef}
                logs={logs}
                isProcessing={isProcessing}
                reversedLogs={reversedLogs}
                getConfidenceLevel={getConfidenceLevel}
            />
        </div>
    );
};

export default DetectionSidebar;
