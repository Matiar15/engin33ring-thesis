import abc


class StitcherPort(abc.ABC):
    @abc.abstractmethod
    async def stitch(
        self, video_name: str, user_id: str, frames: list[tuple[str, str]]
    ) -> str:
        """"""
