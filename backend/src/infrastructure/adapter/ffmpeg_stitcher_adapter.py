import asyncio
import logging
import pathlib
import shutil
import opentelemetry.trace
import PIL.Image
import PIL.ImageDraw

import ffmpeg

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
        frames_location = f"{self.temporary_storage}/{user_id}"
        _logger.info(f"Stitching {len(frames)} frames")

        _logger.info("Creating temporary directory for user: %s..." % user_id)
        user_directory = pathlib.Path(f"{self.temporary_storage}/{user_id}")
        await asyncio.to_thread(
            user_directory.mkdir,
            exist_ok=True,
            parents=True,
        )
        _logger.info("Temporary directory created: %s" % user_directory)

        _logger.info("Downloading frames...")
        images = await asyncio.gather(
            *[
                self.long_term_storage_port.download_file(
                    file_id=frame.id,
                    bucket_name="engin33ring-thesis-frames",
                    from_location=frame.frame_url,
                    to_location=frames_location,
                )
                for frame in frames
            ]
        )
        _logger.info(f"Frames downloaded: {images}")

        _logger.info("Adding bounding boxes to frames...")
        await asyncio.to_thread(self._add_bounding_boxes, images, frames)

        _logger.info("Starting stitching...")
        await asyncio.to_thread(self._render_video, video_name, frames_location)
        _logger.info(f"Stitching completed!")

        _logger.info("Uploading video to long term storage...")
        video_url = await self._store_video(
            video_name=video_name,
            naming_strategy=f"{user_id}/",
        )
        _logger.info("Video uploaded to long term storage: %s" % video_url)

        _logger.info("Removing temporary directory...")
        await asyncio.to_thread(shutil.rmtree, user_directory)
        _logger.info("Temporary directory removed: %s" % user_directory)

        return video_url

    @staticmethod
    @_tracer.start_as_current_span("FFMpegStitcherAdapter.add_bounding_boxes")
    def _add_bounding_boxes(image_paths: list[str], frames: list[Frame]) -> None:
        frame_map = {frame.id: frame for frame in frames}
        for path in image_paths:
            file_name = pathlib.Path(path).stem
            # file_id is the part before the last underscore (if uuid contains underscore, it might be tricky)
            # but usually it's {file_id}_{uuid}
            if "_" in file_name:
                file_id = file_name.rsplit("_", 1)[0]
            else:
                file_id = file_name

            frame = frame_map.get(file_id)
            if not frame or not frame.sign or frame.x is None or frame.y is None:
                continue

            with PIL.Image.open(path) as img:
                draw = PIL.ImageDraw.Draw(img)
                w = frame.width or 100
                h = frame.height or 100
                shape = [frame.x, frame.y, frame.x + w, frame.y + h]
                draw.rectangle(shape, outline="red", width=5)
                draw.text((frame.x, frame.y - 20), frame.sign, fill="red")
                img.save(path)

    @staticmethod
    @_tracer.start_as_current_span("FFMpegStitcherAdapter.render_video")
    def _render_video(
        video_name: str,
        frames_location: str,
    ) -> None:
        (
            ffmpeg
            .input(f"{frames_location}/*.jpg", pattern_type="glob", framerate=1)
            .filter("scale", "min(1920,iw)", "-2")
            .output(
                video_name,
                vcodec="libx264",
                pix_fmt="yuv420p",
                r=30
            )
            .run()
        )

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
