import abc
import typing

from backend.src.frame.domain.frame import Frame

T = typing.TypeVar("T")


class FramePort(abc.ABC):
    @abc.abstractmethod
    async def create(self, frame: Frame) -> str:
        """Create a new domain object. Returns ID of the created object."""
