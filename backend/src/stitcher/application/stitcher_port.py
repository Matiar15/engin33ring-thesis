import abc


from backend.src.frame.domain.frame import Frame


class StitcherPort(abc.ABC):
    @abc.abstractmethod
    async def stitch(
        self,
        video_name: str,
        user_id: str,
        frames: list[Frame],
    ) -> str:
        """"""
