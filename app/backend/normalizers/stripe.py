from datetime import datetime, timezone
from decimal import Decimal

from .base import BaseNormalizer
from ..schemas.processed_event import ProcessedEvent
from ..schemas.raw_event import RawEvent


class StripeNormalizer(BaseNormalizer):
    def normalize(self, raw_event: RawEvent) -> ProcessedEvent:
        payload = raw_event.payload

        data = payload["data"]["object"]

        charge = data["charges"]["data"][0]

        amount = Decimal(data["amount"]) / 100
        fee = Decimal(data.get("application_fee_amount", 0)) / 100

        provider_created = datetime.fromtimestamp(
            payload["created"],
            tz=timezone.utc,
        )

        latency_ms = int(
            (
                raw_event.received_at - provider_created
            ).total_seconds() * 1000
        )

        return ProcessedEvent(
            event_id=payload["id"],
            provider="stripe",
            external_event_id=payload["id"],
            event_type=payload["type"],
            status=data["status"],
            amount=amount,
            currency=data["currency"].upper(),
            fee=fee,
            net_amount=amount - fee,
            payment_id=data["id"],
            order_id=data["metadata"].get("order_id"),
            customer_id=charge.get("receipt_email"),
            failure_reason=charge.get("failure_message"),
            provider_created_at=provider_created,
            received_at=raw_event.received_at,
            processed_at=datetime.now(timezone.utc),
            latency_ms=latency_ms,
        )