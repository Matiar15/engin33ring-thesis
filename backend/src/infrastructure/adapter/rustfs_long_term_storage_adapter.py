import asyncio
import typing
import uuid

from botocore.client import BaseClient

from backend.src.long_term_storage.application.long_term_storage_port import (
    LongTermStoragePort,
)


class RustFSLongTermStorageAdapter(LongTermStoragePort):
    def __init__(self, client: BaseClient):
        self.client = client

    async def store_file(
        self,
        file: typing.BinaryIO,
        bucket_name: str,
        naming_strategy: str,
    ) -> str:
        file_id = str(uuid.uuid4())
        object_name = f"{naming_strategy}_{file_id}.jpg"

        await asyncio.to_thread(
            self.client.upload_fileobj,  # type: ignore
            Fileobj=file,
            Bucket=bucket_name,
            Key=object_name,
            ExtraArgs={
                "ContentType": "image/jpeg",
            },
        )

        return object_name
