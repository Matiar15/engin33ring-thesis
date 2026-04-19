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
from backend.src.frame.domain.frame import Frame
import datetime


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
    frames = [
        Frame(id="f1", frame_url="url1", created_at=datetime.datetime.now()),
        Frame(id="f2", frame_url="url2", created_at=datetime.datetime.now()),
    ]

    mock_storage_port.download_file.side_effect = ["/tmp/f1.jpg", "/tmp/f2.jpg"]
    mock_storage_port.store_file.return_value = "http://storage.com/video.mp4"

    with (
        patch("pathlib.Path.mkdir") as mock_mkdir,
        patch("shutil.rmtree") as mock_rmtree,
        patch("os.remove") as mock_remove,
        patch(
            "backend.src.infrastructure.adapter.ffmpeg_stitcher_adapter.FFMpegStitcherAdapter._prepare_frames"
        ) as mock_prepare,
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
        assert mock_rmtree.called

        # Verify downloads
        assert mock_storage_port.download_file.call_count == 2
        mock_storage_port.download_file.assert_any_call(
            file_id="f1",
            bucket_name="engin33ring-thesis-frames",
            from_location="url1",
            to_location=f"/tmp/{user_id}_{video_name}",
        )

        # Verify upload
        mock_storage_port.store_file.assert_called_once()
        call_args = mock_storage_port.store_file.call_args[1]
        assert call_args["bucket_name"] == "test-videos"
        assert call_args["naming_strategy"] == f"{user_id}/"
        assert call_args["format"] == "mp4"


@pytest.mark.asyncio
async def test_draw_bounding_box_converts_percentages_to_pixels(adapter):
    frame = Frame(
        id="f1",
        frame_url="url1",
        created_at=datetime.datetime.now(),
        sign="speed_limit_30",
        x=10.0,
        y=20.0,
        width=50.0,
        height=25.0,
    )

    img = MagicMock()
    img.size = (640, 480)

    with patch("PIL.ImageDraw.Draw") as mock_draw_cls:
        mock_drawer = MagicMock()
        mock_draw_cls.return_value = mock_drawer

        adapter._draw_bounding_box(img, frame)

        expected_x = 10.0 / 100 * 640  # 64.0
        expected_y = 20.0 / 100 * 480  # 96.0
        expected_w = 50.0 / 100 * 640  # 320.0
        expected_h = 25.0 / 100 * 480  # 120.0

        mock_drawer.rectangle.assert_called_once_with(
            [expected_x, expected_y, expected_x + expected_w, expected_y + expected_h],
            outline="red",
            width=5,
        )
        mock_drawer.text.assert_called_once_with(
            (expected_x, expected_y - 20),
            "speed_limit_30",
            fill="red",
        )


@pytest.mark.asyncio
async def test_draw_bounding_box_skips_frame_without_sign(adapter):
    frame = Frame(
        id="f1",
        frame_url="url1",
        created_at=datetime.datetime.now(),
    )

    img = MagicMock()
    img.size = (640, 480)

    with patch("PIL.ImageDraw.Draw") as mock_draw_cls:
        adapter._draw_bounding_box(img, frame)

        mock_draw_cls.assert_not_called()
