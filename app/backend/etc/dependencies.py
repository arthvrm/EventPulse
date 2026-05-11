from fastapi import Request
from app.backend.schemas.contexts import RequestContext


def get_context(request: Request) -> RequestContext:
    ctx = getattr(request.state, "context", None)
    if ctx is None:
        raise RuntimeError("RequestContext not found. Is middleware enabled?")
    return ctx
