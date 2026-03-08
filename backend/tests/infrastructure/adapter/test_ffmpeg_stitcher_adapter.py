import pytest
from unittest.mock import AsyncMock, MagicMock, patch, mock_open

from backend.src.infrastructure.adapter.ffmpeg_stitcher_adapter import (
    FFMpegStitcherAdapter,
)
from backend.src.settings import (
    Settings,
    StitcherSettings,
    DatabaseSettings,
    LongTermStorageSettings,
)


@pytest.fixture
def mock_settings():
    settings = MagicMock(spec=Settings)
    settings.stitcher = StitcherSettings(
        temporary_dir="/tmp",
        bucket_name="test-videos",
    )
    settings.database = DatabaseSettings(
        protocol="tmp",
        user="user",
        password="pass",
        host="test",
        name="test",
    )
    settings.long_term_storage = LongTermStorageSettings(
        url="test",
        user="user",
        password="pass",
    )
    return settings


@pytest.fixture
def mock_storage_port():
    return AsyncMock()


@pytest.fixture
def adapter(mock_settings, mock_storage_port):
    return FFMpegStitcherAdapter(mock_storage_port, mock_settings)


@pytest.mark.asyncio
async def test_stitch_success(adapter, mock_storage_port):
    # Given
    video_name = "analysis_123"
    user_id = "user_456"
    frames = [("f1", "url1"), ("f2", "url2")]

    mock_storage_port.download_file.side_effect = ["/tmp/f1.jpg", "/tmp/f2.jpg"]
    mock_storage_port.store_file.return_value = "http://storage.com/video.mp4"

    with (
        patch("pathlib.Path.mkdir") as mock_mkdir,
        patch("pathlib.Path.rmdir") as mock_rmdir,
        patch(
            "backend.src.infrastructure.adapter.ffmpeg_stitcher_adapter.FFMpegStitcherAdapter._render_video"
        ) as mock_render,
        patch("builtins.open", mock_open(read_data=b"video data")),
    ):
        # When
        result = await adapter.stitch(video_name, user_id, frames)

        # Then
        assert result == "http://storage.com/video.mp4"
        assert mock_mkdir.called
        assert mock_render.called
        assert mock_rmdir.called

        # Verify downloads
        assert mock_storage_port.download_file.call_count == 2
        mock_storage_port.download_file.assert_any_call(
            file_id="f1",
            bucket_name="engin33ring-thesis-frames",
            from_location="url1",
            to_location=f"/tmp/stitcher/{user_id}",
        )

        # Verify upload
        mock_storage_port.store_file.assert_called_once()
        call_args = mock_storage_port.store_file.call_args[1]
        assert call_args["bucket_name"] == "test-videos"
        assert call_args["naming_strategy"] == f"{user_id}/"
        assert call_args["format"] == "mp4"
