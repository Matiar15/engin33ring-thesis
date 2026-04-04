import asyncio
import typing
import uuid
import opentelemetry.trace

from botocore.client import BaseClient

from backend.src.long_term_storage.application.long_term_storage_port import (
    LongTermStoragePort,
)


_tracer = opentelemetry.trace.get_tracer(__name__)


class RustFSLongTermStorageAdapter(LongTermStoragePort):
    def __init__(self, client: BaseClient):
        self.client = client

    @_tracer.start_as_current_span("RustFSLongTermStorageAdapter.store_file")
    async def store_file(
        self,
        file: typing.BinaryIO,
        bucket_name: str,
        naming_strategy: str,
        format: str,
    ) -> str:
        file_id = str(uuid.uuid4())
        object_name = f"{naming_strategy}{file_id}.{format}"

        await asyncio.to_thread(
            self.client.upload_fileobj,  # type: ignore
            Fileobj=file,
            Bucket=bucket_name,
            Key=object_name,
            ExtraArgs={"ContentType": "image/jpeg" if format == "jpg" else "video/mp4"},
        )

        return object_name

    @_tracer.start_as_current_span("RustFSLongTermStorageAdapter.download_file")
    async def download_file(
        self,
        file_id: str,
        from_location: str,
        bucket_name: str,
        to_location: str,
    ) -> str:
        def _download(file_id_: str) -> str:
            fully_qualified_to_location = (
                f"{to_location}/{file_id_}_{str(uuid.uuid4())}.jpg"
            )
            with open(fully_qualified_to_location, "wb") as f:
                self.client.download_fileobj(  # type: ignore
                    Bucket=bucket_name, Key=from_location, Fileobj=f
                )

            return fully_qualified_to_location

        return await asyncio.to_thread(
            _download,
            file_id_=file_id,
        )
