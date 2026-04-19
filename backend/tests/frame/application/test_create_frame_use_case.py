from datetime import datetime
import pytest
import io
import fastapi
from unittest.mock import AsyncMock, MagicMock
from backend.src.frame.application.create_frame_use_case import CreateFrameUseCase
from backend.src.frame.api.model import FramePayload, FrameResponse
from backend.src.frame.domain.detection import DetectionResult
from backend.src.analysis.domain.analysis import Analysis


@pytest.fixture
def mock_analysis_port():
    return AsyncMock()


@pytest.fixture
def mock_storage_port():
    return AsyncMock()


@pytest.fixture
def mock_detection_port():
    port = AsyncMock()
    port.detect.return_value = DetectionResult(
        sign_name="speed_limit_30",
        confidence=0.95,
        x=15.6,
        y=13.3,
        width=18.75,
        height=25.0,
    )
    return port


@pytest.fixture
def use_case(mock_analysis_port, mock_storage_port, mock_detection_port):
    return CreateFrameUseCase(
        analysis_port=mock_analysis_port,
        long_term_storage_port=mock_storage_port,
        detection_port=mock_detection_port,
    )


@pytest.mark.asyncio
async def test_create_frame_success(
    use_case, mock_analysis_port, mock_storage_port, mock_detection_port
):
    # Given
    mock_file = MagicMock(spec=fastapi.UploadFile)
    mock_file.file = io.BytesIO(b"fake data")
    mock_file.read = AsyncMock(return_value=b"fake data")
    mock_file.seek = AsyncMock()

    payload = FramePayload(
        user_id="user123",
        incoming_id="frame_in_1",
        frame=mock_file,
        analysis_id="analysis_abc",
    )

    # Mock finding existing analysis
    mock_analysis_port.get_one.return_value = Analysis(
        id="analysis_abc",
        user_id="user123",
        status="created",
        modified_at=datetime.now(),
    )

    # Mock file storage
    mock_storage_port.store_file.return_value = "http://storage.com/frame.jpg"

    # When
    response = await use_case.create(payload)

    # Then
    assert isinstance(response, FrameResponse)
    assert response.sign == "SPEED_LIMIT_30"
    assert response.confidence == 95

    # Verify detection was called
    mock_detection_port.detect.assert_called_once_with(b"fake data")

    # Verify analysis validation call
    mock_analysis_port.get_one.assert_called_once_with(
        id="analysis_abc", user_id="user123", statuses=["created", "processing"]
    )

    # Verify storage call
    mock_storage_port.store_file.assert_called_once()

    # Verify analysis update call
    mock_analysis_port.update.assert_called_once()
    update_kwargs = mock_analysis_port.update.call_args[1]
    assert update_kwargs["id"] == "analysis_abc"
    assert update_kwargs["status"] == "processing"
    assert update_kwargs["frame"].id == "frame_in_1"
    assert update_kwargs["frame"].frame_url == "http://storage.com/frame.jpg"


@pytest.mark.asyncio
async def test_create_frame_no_detection(
    mock_analysis_port, mock_storage_port, mock_detection_port
):
    # Given — detection returns None (no sign found)
    mock_detection_port.detect.return_value = None

    use_case = CreateFrameUseCase(
        analysis_port=mock_analysis_port,
        long_term_storage_port=mock_storage_port,
        detection_port=mock_detection_port,
    )

    mock_file = MagicMock(spec=fastapi.UploadFile)
    mock_file.file = io.BytesIO(b"fake data")
    mock_file.read = AsyncMock(return_value=b"fake data")
    mock_file.seek = AsyncMock()

    payload = FramePayload(
        user_id="user123",
        incoming_id="frame_in_1",
        frame=mock_file,
        analysis_id="analysis_abc",
    )

    mock_analysis_port.get_one.return_value = Analysis(
        id="analysis_abc",
        user_id="user123",
        status="created",
        modified_at=datetime.now(),
    )
    mock_storage_port.store_file.return_value = "http://storage.com/frame.jpg"

    # When
    response = await use_case.create(payload)

    # Then
    assert isinstance(response, FrameResponse)
    assert response.sign == "NO_DETECTION"
    assert response.confidence == 0


@pytest.mark.asyncio
async def test_create_frame_analysis_not_found(use_case, mock_analysis_port):
    # Given
    mock_file = MagicMock(spec=fastapi.UploadFile)
    payload = FramePayload(
        user_id="user123",
        incoming_id="frame_in_1",
        frame=mock_file,
        analysis_id="non_existent",
    )

    # Mock analysis not found
    mock_analysis_port.get_one.return_value = None

    # When / Then
    with pytest.raises(
        ValueError, match="Analysis with id: non_existent does not exist."
    ):
        await use_case.create(payload)
