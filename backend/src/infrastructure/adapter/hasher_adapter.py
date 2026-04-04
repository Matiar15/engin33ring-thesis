import pwdlib

from backend.src.hasher.application.hasher_port import HasherPort


class HasherAdapter(HasherPort):
    def __init__(
        self,
    ):
        self.password_hash = pwdlib.PasswordHash.recommended()

    async def hash(self, text: str) -> str:
        return self.password_hash.hash(text)

    async def verify(self, text: str, hashed_text: str) -> bool:
        return self.password_hash.verify(text, hashed_text)
