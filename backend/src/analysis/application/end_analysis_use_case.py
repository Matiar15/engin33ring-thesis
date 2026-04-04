import datetime
import logging

from backend.src.analysis.api.model import EndAnalysisPayload
from backend.src.analysis.application.analysis_port import AnalysisPort
from backend.src.stitcher.application.stitcher_port import StitcherPort

_logger = logging.getLogger(__name__)


class EndAnalysisUseCase:
    def __init__(
        self,
        analysis_port: AnalysisPort,
        stitcher_port: StitcherPort,
    ):
        self.analysis_port = analysis_port
        self.stitcher_port = stitcher_port

    async def end(
        self,
        analysis_payload: EndAnalysisPayload,
        user_id: str,
    ) -> None:
        _logger.info(f"Ending analysis for user: {user_id}...")
        analysis = await self.analysis_port.get_one_and_update(
            id=analysis_payload.id,
            user_id=user_id,
            statuses=["processing"],
            status="stitching",
        )

        if not analysis:
            leftover_analysis = await self.analysis_port.get_one_and_update(
                id=analysis_payload.id,
                user_id=user_id,
                statuses=["stitching"],
                modified_at=datetime.datetime.now() - datetime.timedelta(minutes=5),
                status="stitching",
            )

            if not leftover_analysis:
                raise ValueError(
                    f"Analysis with id: {analysis_payload.id} does not exist."
                )

            analysis = leftover_analysis

        if not analysis.frames:
            raise ValueError(
                f"No frames found for analysis with id: {analysis_payload.id}."
            )

        frame_urls = [(frame.id, frame.frame_url) for frame in analysis.frames]

        _logger.info(f"Stitching frames...")
        video = await self.stitcher_port.stitch(
            video_name=analysis.id,  # type: ignore
            user_id=analysis.user_id,
            frames=frame_urls,
        )

        await self.analysis_port.update(
            id=analysis.id,  # type: ignore
            status="completed",
            video_url=video,
        )

        _logger.info(f"Analysis ended!")
        return None
