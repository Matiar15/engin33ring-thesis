import logging

import boto3
from botocore.client import BaseClient
from botocore.config import Config

from backend.src.settings import Settings

_logger = logging.getLogger(__name__)


def rustfs_config(settings: Settings) -> BaseClient:
    _logger.info("Connecting to RustFS...")

    client = boto3.client(
        "s3",
        endpoint_url=settings.long_term_storage.url,
        aws_access_key_id=settings.long_term_storage.user,
        aws_secret_access_key=settings.long_term_storage.password,
        config=Config(signature_version="s3v4"),
    )

    _logger.info("Connected to RustFS.")
    return client
