from datetime import datetime
from decimal import Decimal
from typing import Any, Dict

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.schemas.payment import Payment
from app.backend.schemas.processed_event import ProcessedEvent
from app.backend.schemas.raw_event import RawEvent

from app.backend.db.models import PaymentModel, ProcessedEventModel, RawEventModel


class EventRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_raw_event(self, raw_event: RawEvent) -> None:
        model = RawEventModel(
            internal_event_id=raw_event.internal_event_id,
            provider=raw_event.provider,
            external_event_id=raw_event.external_event_id,
            event_type=raw_event.event_type,
            raw_body=raw_event.raw_body.decode() if isinstance(raw_event.raw_body, bytes) else raw_event.raw_body,
            headers=raw_event.headers,
            query_params=raw_event.query_params,
            signature=raw_event.signature,
            signature_verified=raw_event.signature_verified,
            request_id=raw_event.request_id,
            client_ip=raw_event.client_ip,
            payload=raw_event.payload,
            received_at=raw_event.received_at,
        )
        self.session.add(model)
        await self.session.commit()

    async def is_processed(self, event_id: str) -> bool:
        stmt = select(ProcessedEventModel).where(ProcessedEventModel.event_id == event_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def save_processed_event(self, event: ProcessedEvent) -> None:
        if not await self.is_processed(event.event_id):
            model = ProcessedEventModel(
                provider=event.provider,
                payment_id=event.payment_id,
                event_id=event.event_id,
                event_type=event.event_type,
                status=event.status,
                amount=event.amount,
                currency=event.currency,
                fee=event.fee,
                net_amount=event.net_amount,
                order_id=event.order_id,
                customer_id=event.customer_id,
                failure_reason=event.failure_reason,
                processing_error=event.processing_error,
                provider_created_at=event.provider_created_at,
                received_at=event.received_at,
                processed_at=event.processed_at,
                latency_ms=event.latency_ms,
            )
            self.session.add(model)
            await self.session.commit()

    async def get_payment(self, payment_id: str) -> Payment | None:
        stmt = select(PaymentModel).where(PaymentModel.payment_id == payment_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            return Payment(
                provider=model.provider,
                payment_id=model.payment_id,
                status=model.status,
                amount=model.amount,
                currency=model.currency,
                fee=model.fee,
                net_amount=model.net_amount,
                order_id=model.order_id,
                customer_id=model.customer_id,
                created_at=model.created_at,
                updated_at=model.updated_at,
                last_event_id=model.last_event_id,
            )
        return None

    async def save_or_update_payment(self, payment: Payment) -> None:
        existing = await self.get_payment(payment.payment_id)
        if existing:
            # Update existing
            stmt = select(PaymentModel).where(PaymentModel.payment_id == payment.payment_id)
            result = await self.session.execute(stmt)
            model = result.scalar_one()
            model.status = payment.status
            model.amount = payment.amount
            model.currency = payment.currency
            model.fee = payment.fee
            model.net_amount = payment.net_amount
            model.order_id = payment.order_id
            model.customer_id = payment.customer_id
            model.updated_at = payment.updated_at
            model.last_event_id = payment.last_event_id
        else:
            # Create new
            model = PaymentModel(
                provider=payment.provider,
                payment_id=payment.payment_id,
                status=payment.status,
                amount=payment.amount,
                currency=payment.currency,
                fee=payment.fee,
                net_amount=payment.net_amount,
                order_id=payment.order_id,
                customer_id=payment.customer_id,
                created_at=payment.created_at,
                updated_at=payment.updated_at,
                last_event_id=payment.last_event_id,
            )
            self.session.add(model)
        await self.session.commit()
