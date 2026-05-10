from datetime import datetime, timezone
from decimal import Decimal

from .base import BaseNormalizer
from schemas.processed_event import ProcessedEvent
from schemas.raw_event import RawEvent


class PayPalNormalizer(BaseNormalizer):
    def normalize(self, raw_event: RawEvent) -> ProcessedEvent:
        payload = raw_event.payload
        resource = payload["resource"]

        gross = (
            resource.get("seller_receivable_breakdown", {})
            .get("gross_amount", {})
            .get("value")
        )

        fee_value = (
            resource.get("seller_receivable_breakdown", {})
            .get("paypal_fee", {})
            .get("value")
        )

        net = (
            resource.get("seller_receivable_breakdown", {})
            .get("net_amount", {})
            .get("value")
        )

        amount = Decimal(gross or resource["amount"]["value"])

        fee = Decimal(fee_value) if fee_value else None

        net_amount = Decimal(net) if net else None

        provider_created = datetime.fromisoformat(
            payload["create_time"].replace("Z", "+00:00")
        )

        latency_ms = int(
            (
                raw_event.received_at - provider_created
            ).total_seconds() * 1000
        )

        return ProcessedEvent(
            provider="paypal",
            payment_id=resource["id"],
            event_id=payload["id"],
            event_type=payload["event_type"],
            status=resource["status"],
            amount=amount,
            currency=resource["amount"]["currency_code"],
            fee=fee,
            net_amount=net_amount,
            order_id=resource.get("custom_id"),
            customer_id=resource["payer"]["payer_id"],
            failure_reason=(
                resource.get("status_details", {})
                .get("reason")
            ),
            provider_created_at=provider_created,
            received_at=raw_event.received_at,
            processed_at=datetime.now(timezone.utc),
            latency_ms=latency_ms,
        )