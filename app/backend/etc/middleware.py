import logging
import uuid
from pathlib import Path
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from schemas.contexts import RequestContext


logger = logging.getLogger(str(Path(__name__)))

class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())

        client_ip = request.client.host if request.client else None
        
        # Read body once
        body = await request.body()

        # Store context
        request.state.context = RequestContext(
            request_id=request_id,
            client_ip=client_ip,
            headers=dict(request.headers),
            query_params=dict(request.query_params),
            raw_body=body,
        )

        response = await call_next(request)
        
        logger.info("Request completed")

        return response
