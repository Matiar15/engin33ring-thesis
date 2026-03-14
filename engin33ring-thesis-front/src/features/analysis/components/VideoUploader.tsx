import { Upload, Film, AlertCircle } from 'lucide-react';
import { useFileDrop } from '@/features/analysis/hooks/useFileDrop';

const SUPPORTED_VIDEO_CODECS = [
	'video/mp4; codecs="avc1.42E01E, mp4a.40.2"',
	'video/mp4; codecs="avc1.4D401E, mp4a.40.2"',
	'video/mp4; codecs="avc1.64001E, mp4a.40.2"',
];

const canPlayAny = () => {
	const testVideo = document.createElement('video');
	return SUPPORTED_VIDEO_CODECS.some(codec => testVideo.canPlayType(codec) !== '');
};

const validateVideoFile = (file: File): string | null => {
	if (!file.type.startsWith('video/mp4')) {
		return 'Please upload a valid video file';
	}
	if (!canPlayAny()) {
		return 'This browser cannot decode the supported codecs (H.264/AAC or VP8/VP9).';
	}
	return null;
};

interface VideoUploaderProps {
	onVideoSelect: (file: File, url: string) => void;
}

const VideoUploader = ({ onVideoSelect }: VideoUploaderProps) => {
	const { isDragging, error, dragProps, handleFileInput } = useFileDrop({
		accept: 'video/mp4',
		onFileSelect: onVideoSelect,
		validateFile: validateVideoFile,
	});

	return (
		<div className="flex flex-col items-center justify-center h-full p-4 sm:p-6 lg:p-8 animate-fade-in">
			<div
				{...dragProps}
				className={`relative w-full max-w-2xl sm:max-w-3xl lg:max-w-4xl aspect-video rounded-2xl border-2 border-dashed transition-all duration-300 flex flex-col items-center justify-center cursor-pointer overflow-hidden group ${
					isDragging
						? 'border-primary bg-primary/10 scale-[1.02]'
						: 'border-border hover:border-primary/50 hover:bg-muted/30'
				}`}
			>
				{/* Animated scan line */}
				<div className={`absolute inset-0 scan-line pointer-events-none ${isDragging ? 'opacity-100' : 'opacity-0 group-hover:opacity-50'}`} />

				{/* Corner decorations */}
				<div className="absolute top-0 left-0 w-8 h-8 border-t-2 border-l-2 border-primary/50 rounded-tl-lg" />
				<div className="absolute top-0 right-0 w-8 h-8 border-t-2 border-r-2 border-primary/50 rounded-tr-lg" />
				<div className="absolute bottom-0 left-0 w-8 h-8 border-b-2 border-l-2 border-primary/50 rounded-bl-lg" />
				<div className="absolute bottom-0 right-0 w-8 h-8 border-b-2 border-r-2 border-primary/50 rounded-br-lg" />

				<input
					type="file"
					accept="video/*"
					onChange={handleFileInput}
					className="absolute inset-0 opacity-0 cursor-pointer"
				/>

				<div className={`p-5 sm:p-6 rounded-full bg-primary/10 mb-4 sm:mb-6 transition-all duration-300 ${isDragging ? 'scale-110 bg-primary/20' : 'group-hover:scale-105'}`}>
					{isDragging ? (
						<Film className="w-10 h-10 sm:w-12 sm:h-12 text-primary animate-pulse" />
					) : (
						<Upload className="w-10 h-10 sm:w-12 sm:h-12 text-primary" />
					)}
				</div>

				<h3 className="text-lg sm:text-xl font-display font-semibold text-foreground mb-2">
					{isDragging ? 'Drop Video Here' : 'Upload Video for Analysis'}
				</h3>
				<p className="text-muted-foreground text-center max-w-md text-sm sm:text-base">
					Drag and drop a video file or click to browse.
					<br />
					<span className="text-xs sm:text-sm">Supports MP4, WebM, MOV</span>
				</p>

				{error && (
					<div className="flex items-center gap-2 mt-4 px-4 py-2 bg-destructive/10 border border-destructive/30 rounded-lg text-destructive">
						<AlertCircle className="w-4 h-4" />
						<span className="text-sm">{error}</span>
					</div>
				)}
			</div>

			<div className="mt-6 sm:mt-8 flex flex-col items-center gap-3 text-muted-foreground text-sm sm:flex-row sm:gap-6">
				<div className="flex items-center gap-2">
					<div className="w-2 h-2 rounded-full bg-neon-green animate-pulse" />
					<span>Neural Network Ready</span>
				</div>
				<div className="flex items-center gap-2">
					<div className="w-2 h-2 rounded-full bg-primary animate-pulse" />
					<span>15+ Sign Types Supported</span>
				</div>
			</div>
		</div>
	);
};

export default VideoUploader;
