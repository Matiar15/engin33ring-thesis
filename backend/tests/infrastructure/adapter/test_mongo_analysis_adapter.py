import pytest
import bson
from unittest.mock import AsyncMock, MagicMock
from backend.src.infrastructure.adapter.mongo_analysis_adapter import (
    MongoAnalysisAdapter,
)
from backend.src.analysis.domain.analysis import Analysis
from backend.src.frame.domain.frame import Frame
from datetime import datetime


@pytest.fixture
def mock_collection():
    return AsyncMock()


@pytest.fixture
def mock_db(mock_collection):
    db = MagicMock()
    db.__getitem__.return_value = mock_collection
    return db


@pytest.fixture
def adapter(mock_db):
    return MongoAnalysisAdapter(mock_db)


@pytest.mark.asyncio
async def test_create_analysis(adapter, mock_collection):
    # Given
    analysis = Analysis(user_id="user123", status="pending")
    mock_collection.insert_one.return_value = MagicMock(inserted_id=bson.ObjectId())

    # When
    inserted_id = await adapter.create(analysis)

    # Then
    assert isinstance(inserted_id, str)
    mock_collection.insert_one.assert_called_once()
    call_args = mock_collection.insert_one.call_args[0][0]
    assert call_args["user_id"] == "user123"
    assert call_args["status"] == "pending"


@pytest.mark.asyncio
async def test_get_one_found(adapter, mock_collection):
    # Given
    obj_id = bson.ObjectId()
    id_str = str(obj_id)
    user_id = "user123"
    mock_collection.find_one.return_value = {
        "_id": obj_id,
        "user_id": user_id,
        "status": "completed",
        "frames": [],
    }

    # When
    result = await adapter.get_one(id_str, user_id)

    # Then
    assert result is not None
    assert result.id == id_str
    assert result.user_id == user_id
    mock_collection.find_one.assert_called_once_with(
        {"_id": obj_id, "user_id": user_id}
    )


@pytest.mark.asyncio
async def test_get_one_with_statuses(adapter, mock_collection):
    # Given
    obj_id = bson.ObjectId()
    id_str = str(obj_id)
    user_id = "user123"
    statuses = ["completed", "failed"]
    mock_collection.find_one.return_value = {
        "_id": obj_id,
        "user_id": user_id,
        "status": "completed",
    }

    # When
    await adapter.get_one(id_str, user_id, statuses=statuses)

    # Then
    mock_collection.find_one.assert_called_once_with(
        {"_id": obj_id, "user_id": user_id, "status": {"$in": statuses}}
    )


@pytest.mark.asyncio
async def test_update_status(adapter, mock_collection):
    # Given
    obj_id = bson.ObjectId()
    id_str = str(obj_id)
    new_status = "processed"

    # When
    await adapter.update(id_str, status=new_status)

    # Then
    mock_collection.update_one.assert_called_once_with(
        filter={"_id": obj_id}, update={"$set": {"status": new_status}}
    )


@pytest.mark.asyncio
async def test_update_push_frame(adapter, mock_collection):
    # Given
    obj_id = bson.ObjectId()
    id_str = str(obj_id)
    frame = Frame(
        id="frame1", frame_url="http://example.com/1.jpg", created_at=datetime.now()
    )

    # When
    await adapter.update(id_str, frame=frame)

    # Then
    mock_collection.update_one.assert_called_once()
    call_args = mock_collection.update_one.call_args[1]
    assert call_args["filter"] == {"_id": obj_id}
    assert "$push" in call_args["update"]
    assert "frames" in call_args["update"]["$push"]
    assert call_args["update"]["$push"]["frames"]["id"] == "frame1"
