import asyncio
import typing
import uuid

import boto3
from botocore.config import Config

from backend.src.long_term_storage.application.long_term_storage_port import LongTermStoragePort
from backend.src.settings import Settings


class RustFSLongTermStorageAdapter(LongTermStoragePort):
    def __init__(self, settings: Settings):
        self.client = boto3.client(
            "s3",
            endpoint_url=settings.long_term_storage.url,
            aws_access_key_id=settings.long_term_storage.user,
            aws_secret_access_key=settings.long_term_storage.password,
            config=Config(signature_version="s3v4"),
        )

    async def store_file(self, file: typing.BinaryIO, bucket_name: str, naming_strategy: str,) -> str:
        file_id = str(uuid.uuid4())
        object_name = f"{naming_strategy}_{file_id}.jpg"

        await asyncio.to_thread(
            self.client.upload_fileobj,
            Fileobj=file,
            Bucket=bucket_name,
            Key=object_name,
            ExtraArgs={
                "ContentType": "image/jpeg",
            }
        )

        return object_name