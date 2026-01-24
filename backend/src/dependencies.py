import fastapi

from backend.src.metadata.application.metadata_use_case import MetadataUseCase


def get_metadata_use_case(request: fastapi.Request) -> MetadataUseCase:
    use_case: MetadataUseCase = request.app.state.metadata_use_case
    return use_case
