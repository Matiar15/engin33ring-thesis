import pwdlib
import opentelemetry.trace


from backend.src.hasher.application.hasher_port import HasherPort

_tracer = opentelemetry.trace.get_tracer(__name__)

class HasherAdapter(HasherPort):
    def __init__(
        self,
    ):
        self.password_hash = pwdlib.PasswordHash.recommended()

    @_tracer.start_as_current_span("HasherAdapter.hash")
    async def hash(self, text: str) -> str:
        return self.password_hash.hash(text)

    @_tracer.start_as_current_span("HasherAdapter.verify")
    async def verify(self, text: str, hashed_text: str) -> bool:
        return self.password_hash.verify(text, hashed_text)
