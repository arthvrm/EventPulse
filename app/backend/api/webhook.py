import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.schemas.contexts import RequestContext
from app.backend.etc.dependencies import get_context, get_db_session
from app.backend.schemas.raw_event import RawEvent
from app.backend.etc.security import verify_hmac_signature
from app.backend.services.service import WebhookService
from app.backend.db.repository import EventRepository

load_dotenv()

SECRET = os.getenv("WEBHOOK_SECRET")
if not SECRET:
    raise ValueError("WEBHOOK_SECRET is required. Set it in the .env file or environment.")


logger = logging.getLogger(str(Path(__name__)))

router = APIRouter()


@router.post("/webhook")
async def receive_webhook(
    context: RequestContext = Depends(get_context),
    session: AsyncSession = Depends(get_db_session),
):
    logger.info(
        f"Webhook received. id: {context.request_id}",
        extra={
            "request_id": context.request_id,
            "client_ip": context.client_ip,
            "headers": context.headers,
            "query_params": context.query_params,
            "signature": context.headers.get("x-signature"),
        }
    )
    
    # Parse payload
    try:
        payload_dict = context.raw_body.decode("utf-8")
        payload_json = json.loads(payload_dict)
    except Exception as e:
        logger.warning("Failed to parse payload", exc_info=e)
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
    
    # Determine provider
    if "resource_type" in payload_json:
        provider = "paypal"
        external_event_id = payload_json["id"]
        event_type = payload_json["event_type"]
    elif payload_json.get("object") == "event":
        provider = "stripe"
        external_event_id = payload_json["id"]
        event_type = payload_json["type"]
    else:
        logger.warning("Unknown provider")
        raise HTTPException(status_code=400, detail="Unknown provider")
    
    # HMAC verify
    signature_verified = verify_hmac_signature(SECRET, context.raw_body, context.headers.get("x-signature") or "")
    if not signature_verified:
        logger.warning("Invalid HMAC signature")
        raise HTTPException(status_code=401, detail="Invalid signature")
    
    logger.info("Verified HMAC signature")
    
    # Create RawEvent
    raw_event = RawEvent(
        internal_event_id=context.request_id,
        provider=provider,
        external_event_id=external_event_id,
        event_type=event_type,
        raw_body=context.raw_body,
        headers=dict(context.headers),
        query_params=dict(context.query_params),
        signature=context.headers.get("x-signature"),
        signature_verified=signature_verified,
        request_id=context.request_id,
        client_ip=context.client_ip,
        payload=payload_json,
        received_at=datetime.now(timezone.utc),
    )
    
    # Create repo and service
    repo = EventRepository(session)
    service = WebhookService(repo)
    
    # Process
    try:
        await service.process_events(raw_event)
    except Exception as e:
        logger.error("Error processing event", exc_info=e)
        raise HTTPException(status_code=500, detail="Internal error")
    
    logger.info(f"Webhook processed successfully event_id={raw_event.external_event_id}")

    return {"status": "ok"}
