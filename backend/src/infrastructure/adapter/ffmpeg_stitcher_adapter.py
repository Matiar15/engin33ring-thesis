import asyncio
import logging
import pathlib

import ffmpeg

from backend.src.long_term_storage.application.long_term_storage_port import (
    LongTermStoragePort,
)
from backend.src.stitcher.application.stitcher_port import StitcherPort
from backend.src.settings import Settings

_logger = logging.getLogger(__name__)


class FFMpegStitcherAdapter(StitcherPort):
    def __init__(
        self,
        long_term_storage_port: LongTermStoragePort,
        settings: Settings,
    ):
        self.long_term_storage_port = long_term_storage_port
        self.temporary_storage = settings.stitcher.temporary_dir
        self.bucket_name = settings.stitcher.bucket_name

    async def stitch(
        self,
        video_name: str,
        user_id: str,
        frames: list[tuple[str, str]],
    ) -> str:
        video_name = f"{video_name}.mp4"
        frames_location = f"{self.temporary_storage}/{user_id}"
        _logger.info(f"Stitching frames: {frames}")

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
                    file_id=id_,
                    bucket_name="engin33ring-thesis-frames",
                    from_location=url,
                    to_location=frames_location,
                )
                for id_, url in frames
            ]
        )
        _logger.info(f"Frames downloaded: {images}")

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
        await asyncio.to_thread(user_directory.rmdir)
        _logger.info("Temporary directory removed: %s" % user_directory)

        return video_url

    def _render_video(
        self,
        video_name: str,
        frames_location: str,
    ) -> None:
        (
            ffmpeg.input(f"{frames_location}/*.jpg", pattern_type="glob", framerate=30)
            .filter("scale", "min(1920,iw)", "-2")
            .output(
                video_name,
                vcodec="libx264",
                pix_fmt="yuv420p",
            )
            .run()
        )

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
