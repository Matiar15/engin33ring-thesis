import pytest
import datetime
from unittest.mock import AsyncMock, MagicMock
from backend.src.analysis.application.end_analysis_use_case import EndAnalysisUseCase
from backend.src.analysis.api.model import EndAnalysisPayload
from backend.src.analysis.domain.analysis import Analysis
from backend.src.frame.domain.frame import Frame


@pytest.fixture
def mock_analysis_port():
    return AsyncMock()


@pytest.fixture
def mock_stitcher_port():
    return AsyncMock()


@pytest.fixture
def use_case(mock_analysis_port, mock_stitcher_port):
    return EndAnalysisUseCase(
        analysis_port=mock_analysis_port, stitcher_port=mock_stitcher_port
    )


@pytest.mark.asyncio
async def test_end_analysis_success(use_case, mock_analysis_port, mock_stitcher_port):
    # Given
    payload = EndAnalysisPayload(id="analysis_123", user_id="user_456")
    frames = [
        Frame(id="f1", frame_url="url1", created_at=datetime.datetime.now()),
        Frame(id="f2", frame_url="url2", created_at=datetime.datetime.now()),
    ]
    analysis = Analysis(
        id="analysis_123",
        user_id="user_456",
        status="processing",
        modified_at=datetime.datetime.now(),
        frames=frames,
    )

    mock_analysis_port.get_one_and_update.return_value = analysis
    mock_stitcher_port.stitch.return_value = "http://storage.com/video.mp4"

    # When
    await use_case.end(payload)

    # Then
    mock_analysis_port.get_one_and_update.assert_called_once_with(
        id="analysis_123",
        user_id="user_456",
        statuses=["processing"],
        status="stitching",
    )

    mock_stitcher_port.stitch.assert_called_once_with(
        video_name="analysis_123",
        user_id="user_456",
        frames=[("f1", "url1"), ("f2", "url2")],
    )

    mock_analysis_port.update.assert_called_once_with(
        id="analysis_123", status="completed", video_url="http://storage.com/video.mp4"
    )


@pytest.mark.asyncio
async def test_end_analysis_leftover_success(
    use_case, mock_analysis_port, mock_stitcher_port
):
    # Given
    payload = EndAnalysisPayload(id="analysis_123", user_id="user_456")
    frames = [Frame(id="f1", frame_url="url1", created_at=datetime.datetime.now())]
    analysis = Analysis(
        id="analysis_123",
        user_id="user_456",
        status="stitching",
        modified_at=datetime.datetime.now() - datetime.timedelta(minutes=10),
        frames=frames,
    )

    # First call returns None (not processing)
    # Second call returns the leftover analysis
    mock_analysis_port.get_one_and_update.side_effect = [None, analysis]
    mock_stitcher_port.stitch.return_value = "http://storage.com/video.mp4"

    # When
    await use_case.end(payload)

    # Then
    assert mock_analysis_port.get_one_and_update.call_count == 2
    mock_stitcher_port.stitch.assert_called_once()
    mock_analysis_port.update.assert_called_once_with(
        id="analysis_123", status="completed", video_url="http://storage.com/video.mp4"
    )


@pytest.mark.asyncio
async def test_end_analysis_not_found_raises_error(use_case, mock_analysis_port):
    # Given
    payload = EndAnalysisPayload(id="analysis_123", user_id="user_456")
    mock_analysis_port.get_one_and_update.return_value = None

    # When / Then
    with pytest.raises(
        ValueError, match="Analysis with id: analysis_123 does not exist."
    ):
        await use_case.end(payload)


@pytest.mark.asyncio
async def test_end_analysis_no_frames_raises_error(use_case, mock_analysis_port):
    # Given
    payload = EndAnalysisPayload(id="analysis_123", user_id="user_456")
    analysis = Analysis(
        id="analysis_123",
        user_id="user_456",
        status="processing",
        modified_at=datetime.datetime.now(),
        frames=[],
    )
    mock_analysis_port.get_one_and_update.return_value = analysis

    # When / Then
    with pytest.raises(
        ValueError, match="No frames found for analysis with id: analysis_123."
    ):
        await use_case.end(payload)
