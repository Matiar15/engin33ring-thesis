import abc
import typing

T = typing.TypeVar("T")


class DatabasePort(abc.ABC, typing.Generic[T]):
    @abc.abstractmethod
    async def create(self, collection_name: str, domain: T) -> T:
        """Create a new domain object. Returns the created object."""
