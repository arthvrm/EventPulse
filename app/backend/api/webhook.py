import logging
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException

from ..schemas.contexts import RequestContext
from ..etc.dependencies import get_context
from ..schemas.raw_event import RawEvent
from ..etc.security import verify_hmac_signature
from ..services.service import WebhookService
from ..db.repository import EventRepository


logger = logging.getLogger(str(Path(__name__)))

router = APIRouter()

SECRET = "supersecret"

repo = EventRepository()
service = WebhookService(repo)


@router.post("/webhook")
async def receive_webhook(
    context: RequestContext = Depends(get_context),
):
    logger.info(
        f"Webhook received. id: {context.request_id}",
        extra={
            "request_id": context.request_id,
            "client_ip": context.client_ip,
            "headers": context.headers,
            "query_params": context.query_params,
            "signature": context.x_signature,
            "body": context.raw_body.decode("utf-8"),
        }
    )
    
    # HMAC verify
    if not verify_hmac_signature(SECRET, context.raw_body, context.x_signature):
        logger.warning("Invalid HMAC signature")
        raise HTTPException(status_code=401, detail="Invalid signature")
    
    logger.info("Verified HMAC signature")

    # Validation
    try:
        payload = RawEvent.model_validate_json(context.raw_body)
        logger.info("Payload validated")
    except Exception as e:
        logger.warning("Payload validation failed", exc_info=e)
        raise HTTPException(status_code=400, detail="Invalid payload")

    # Process
    try:
        service.process_events(payload)
    except Exception as e:
        logger.error("Error processing event", exc_info=e)
        raise HTTPException(status_code=500, detail="Internal error")
    
    logger.info(f"Webhook processed successfully event_id={payload.event_id}")

    return {"status_code": 200}

