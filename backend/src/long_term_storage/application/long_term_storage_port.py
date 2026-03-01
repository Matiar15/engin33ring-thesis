import abc
import typing


class LongTermStoragePort(abc.ABC):
    @abc.abstractmethod
    async def store_file(self, file: typing.BinaryIO, bucket_name: str, naming_strategy: str) -> str:
        """Store a file in the long-term storage database."""
