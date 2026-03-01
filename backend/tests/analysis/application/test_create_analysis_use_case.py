import pytest
from unittest.mock import AsyncMock
from backend.src.analysis.application.create_analysis_use_case import (
    CreateAnalysisUseCase,
)
from backend.src.analysis.api.model import AnalysisPayload, AnalysisResponse
from backend.src.analysis.domain.analysis import Analysis


@pytest.fixture
def mock_analysis_port():
    return AsyncMock()


@pytest.fixture
def use_case(mock_analysis_port):
    return CreateAnalysisUseCase(analysis_port=mock_analysis_port)


@pytest.mark.asyncio
async def test_create_analysis_success(use_case, mock_analysis_port):
    # Given
    payload = AnalysisPayload(user_id="user_123")
    mock_analysis_port.create.return_value = "generated_id_456"

    # When
    response = await use_case.create(payload)

    # Then
    assert isinstance(response, AnalysisResponse)
    assert response.id == "generated_id_456"

    # Verify port call
    mock_analysis_port.create.assert_called_once()
    call_args = mock_analysis_port.create.call_args[1]["analysis"]
    assert isinstance(call_args, Analysis)
    assert call_args.user_id == "user_123"
    assert call_args.status == "created"
