import os
import asyncio
import logging
import pathlib
import shutil
import subprocess
import opentelemetry.trace
import PIL.Image
import PIL.ImageDraw

from backend.src.long_term_storage.application.long_term_storage_port import (
    LongTermStoragePort,
)
from backend.src.stitcher.application.stitcher_port import StitcherPort
from backend.src.settings import Settings
from backend.src.frame.domain.frame import Frame

_logger = logging.getLogger(__name__)
_tracer = opentelemetry.trace.get_tracer(__name__)


class FFMpegStitcherAdapter(StitcherPort):
    def __init__(
        self,
        long_term_storage_port: LongTermStoragePort,
        settings: Settings,
    ):
        self.long_term_storage_port = long_term_storage_port
        self.temporary_storage = settings.stitcher.temporary_dir
        self.bucket_name = settings.stitcher.bucket_name

    @_tracer.start_as_current_span("FFMpegStitcherAdapter.stitch")
    async def stitch(
        self,
        video_name: str,
        user_id: str,
        frames: list[Frame],
    ) -> str:
        video_name = f"{video_name}.mp4"
        frames_location = (
            f"{self.temporary_storage}/{user_id}_{video_name.replace('.mp4', '')}"
        )
        _logger.info(f"Stitching {len(frames)} frames")

        _logger.info("Creating temporary directory for user: %s..." % user_id)
        user_directory = pathlib.Path(frames_location)
        await asyncio.to_thread(
            user_directory.mkdir,
            exist_ok=True,
            parents=True,
        )
        _logger.info("Temporary directory created: %s" % user_directory)

        sorted_frames = sorted(
            frames,
            key=lambda f: int(f.id) if f.id.isdigit() else float("inf"),
        )

        _logger.info("Downloading frames...")
        images = list(
            await asyncio.gather(
                *[
                    self.long_term_storage_port.download_file(
                        file_id=frame.id,
                        bucket_name="engin33ring-thesis-frames",
                        from_location=frame.frame_url,
                        to_location=frames_location,
                    )
                    for frame in sorted_frames
                ]
            )
        )
        _logger.info(f"Frames downloaded: {images}")

        _logger.info("Preparing frames...")
        await asyncio.to_thread(
            self._prepare_frames, images, sorted_frames, frames_location
        )

        _logger.info("Starting stitching...")
        await asyncio.to_thread(self._render_video, video_name, frames_location)
        _logger.info("Stitching completed!")

        _logger.info("Uploading video to long term storage...")
        video_url = await self._store_video(
            video_name=video_name,
            naming_strategy=f"{user_id}/",
        )
        _logger.info("Video uploaded to long term storage: %s" % video_url)

        _logger.info("Removing temporary directory...")
        await asyncio.to_thread(shutil.rmtree, user_directory)
        await asyncio.to_thread(os.remove, video_name)
        _logger.info("Temporary directory removed: %s" % user_directory)

        return video_url

    @_tracer.start_as_current_span("FFMpegStitcherAdapter.prepare_frames")
    def _prepare_frames(
        self,
        image_paths: list[str],
        frames: list[Frame],
        frames_location: str,
    ) -> None:
        if not image_paths:
            return

        with PIL.Image.open(image_paths[0]) as first_img:
            target_size = (first_img.width // 2 * 2, first_img.height // 2 * 2)

        for i, (path, frame) in enumerate(zip(image_paths, frames), start=1):
            img = PIL.Image.open(path)
            img.load()
            img = img.convert("RGB")  # type: ignore

            if img.size != target_size:
                img = img.resize(target_size, PIL.Image.Resampling.LANCZOS)  # type: ignore

            self._draw_bounding_box(img, frame)

            img.save(os.path.join(frames_location, f"frame_{i:04d}.png"), format="PNG")
            img.close()
            os.remove(path)

    @staticmethod
    @_tracer.start_as_current_span("FFMpegStitcherAdapter.draw_bounding_box")
    def _draw_bounding_box(img: PIL.Image.Image, frame: Frame) -> None:
        if not frame.sign or frame.x is None or frame.y is None:
            return

        img_w, img_h = img.size
        draw = PIL.ImageDraw.Draw(img)

        x = frame.x / 100 * img_w
        y = frame.y / 100 * img_h
        w = (frame.width or 0) / 100 * img_w
        h = (frame.height or 0) / 100 * img_h

        draw.rectangle([x, y, x + w, y + h], outline="red", width=5)
        draw.text((x, max(y - 20, 0)), frame.sign, fill="red")

    @staticmethod
    @_tracer.start_as_current_span("FFMpegStitcherAdapter.render_video")
    def _render_video(
        video_name: str,
        frames_location: str,
    ) -> None:
        result = subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-framerate",
                "10",
                "-i",
                f"{frames_location}/frame_%04d.png",
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-crf",
                "23",
                "-movflags",
                "+faststart",
                video_name,
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(f"ffmpeg failed: {result.stderr}")

    @_tracer.start_as_current_span("FFMpegStitcherAdapter.store_video")
    async def _store_video(
        self,
        video_name: str,
        naming_strategy: str,
    ) -> str:
        file = await asyncio.to_thread(open, video_name, "rb")
        try:
            video_url = await self.long_term_storage_port.store_file(
                file=file,
                bucket_name=self.bucket_name,
                naming_strategy=naming_strategy,
                format="mp4",
            )
        finally:
            await asyncio.to_thread(file.close)

        return video_url
