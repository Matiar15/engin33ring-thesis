import abc
import typing

T = typing.TypeVar("T")


class DatabasePort(abc.ABC, typing.Generic[T]):
    @abc.abstractmethod
    async def create(self, domain: T) -> str:
        """Create a new domain object. Returns ID of the created object."""
