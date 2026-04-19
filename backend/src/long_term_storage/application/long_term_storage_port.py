import abc
import typing


class LongTermStoragePort(abc.ABC):
    @abc.abstractmethod
    async def store_file(
        self,
        file: typing.BinaryIO,
        bucket_name: str,
        naming_strategy: str,
        format: str,
    ) -> str:
        """Store a file in the long-term storage database."""

    @abc.abstractmethod
    async def download_file(
        self,
        file_id: str,
        from_location: str,
        bucket_name: str,
        to_location: str,
    ) -> str:
        """"""

    @abc.abstractmethod
    async def generate_presigned_url(
        self,
        bucket_name: str,
        object_name: str,
        expiration: int = 900,
    ) -> str:
        """"""

    @abc.abstractmethod
    async def generate_presigned_url(
        self,
        bucket_name: str,
        object_name: str,
        expiration: int = 900,
    ) -> str:
        """"""
