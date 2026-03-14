import pytest
import io
import uuid
from unittest.mock import MagicMock, patch
from backend.src.infrastructure.adapter.rustfs_long_term_storage_adapter import (
    RustFSLongTermStorageAdapter,
)


@pytest.fixture
def mock_s3_client():
    return MagicMock()


@pytest.fixture
def adapter(mock_s3_client):
    return RustFSLongTermStorageAdapter(mock_s3_client)


@pytest.mark.asyncio
async def test_store_file(adapter, mock_s3_client):
    # Given
    file_content = b"fake image data"
    file_obj = io.BytesIO(file_content)
    bucket_name = "test-bucket"
    naming_strategy = "user_123"

    # Mock uuid4 to have a predictable name
    fake_uuid = uuid.uuid4()
    with patch("uuid.uuid4", return_value=fake_uuid):
        # When
        object_name = await adapter.store_file(
            file_obj, bucket_name, naming_strategy, format="jpg"
        )

        # Then
        expected_name = f"{naming_strategy}{str(fake_uuid)}.jpg"
        assert object_name == expected_name

        # Check if upload_fileobj was called (via asyncio.to_thread)
        mock_s3_client.upload_fileobj.assert_called_once_with(
            Fileobj=file_obj,
            Bucket=bucket_name,
            Key=expected_name,
            ExtraArgs={
                "ContentType": "image/jpeg",
            },
        )


@pytest.mark.asyncio
async def test_download_file(adapter, mock_s3_client):
    # Given
    file_id = "file123"
    bucket_name = "test-bucket"
    from_location = "path/to/file.jpg"
    to_location = "/tmp/test"

    # Mock uuid4
    fake_uuid = uuid.uuid4()

    with (
        patch("uuid.uuid4", return_value=fake_uuid),
        patch("builtins.open", MagicMock()) as mock_open,
    ):
        # When
        result = await adapter.download_file(
            file_id=file_id,
            from_location=from_location,
            bucket_name=bucket_name,
            to_location=to_location,
        )

        # Then
        expected_path = f"{to_location}/{file_id}_{str(fake_uuid)}.jpg"
        assert result == expected_path

        mock_s3_client.download_fileobj.assert_called_once()
        call_args = mock_s3_client.download_fileobj.call_args[1]
        assert call_args["Bucket"] == bucket_name
        assert call_args["Key"] == from_location
        assert mock_open.call_args[0][0] == expected_path
