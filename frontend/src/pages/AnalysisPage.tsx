import VideoUploader from '@/features/analysis/components/VideoUploader.tsx';
import VideoPlayer from '@/features/analysis/components/VideoPlayer.tsx';
import DetectionSidebar from '@/features/analysis/components/DetectionSidebar.tsx';
import {AnalysisHeader} from '@/features/analysis/components/AnalysisHeader.tsx';
import {useVideoAnalysis} from '@/features/analysis/context';
import VideoControls from "@/features/analysis/components/VideoControls.tsx";

const AnalysisPage = () => {
  const { state, selectVideo, stopAndArchive, reset } = useVideoAnalysis();
  const { videoFile, videoUrl, isProcessing, isFinished, detectionLogs } = state;

  const mainContent = !videoUrl ? (
    <VideoUploader onVideoSelect={selectVideo} />
  ) : (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-full animate-fade-in">
      <div className="lg:col-span-2 flex flex-col gap-4">
        <VideoPlayer
          videoUrl={videoUrl}
          isProcessing={isProcessing}
        />

        <VideoControls
          isProcessing={isProcessing}
          isFinished={isFinished}
          videoFile={videoFile}
          stopAndArchive={stopAndArchive}
          reset={reset}
        />
      </div>
      <div className="lg:col-span-1 h-[calc(100vh-12rem)]">
        <DetectionSidebar logs={detectionLogs} isProcessing={isProcessing} isFinished={isFinished} />
      </div>
    </div>
  );

  return (
    <div className="min-h-screen flex flex-col">
      <AnalysisHeader />
      <main className="flex-1 p-6">
        {mainContent}
      </main>
    </div>
  );
};

export default AnalysisPage;
