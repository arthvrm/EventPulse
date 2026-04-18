import random
from typing import Any, Dict
import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal, ROUND_HALF_UP

from .event_collections import (
    STRIPE_EVENT_STATUS_MAP,
    STRIPE_FAILURE_REASON_MAP,
    NAMES,
    PRODUCTS
)


def money_cents(value: Decimal) -> int:
    return int(value.quantize(Decimal("1"), rounding=ROUND_HALF_UP) * 100)


def generate_payload() -> Dict[str, Any]:
    event_type = random.choice(list(STRIPE_EVENT_STATUS_MAP.keys()))
    status = STRIPE_EVENT_STATUS_MAP[event_type]

    reason = random.choice(
        STRIPE_FAILURE_REASON_MAP.get(event_type, ["none"])
    )

    name = random.choice(NAMES)

    selected_products = random.sample(PRODUCTS, k=random.randint(1, 3))

    total = Decimal("0")

    for _, _, price in selected_products:
        quantity = random.randint(1, 2)
        total += Decimal(str(price)) * quantity

    fee = (total * Decimal("0.029") + Decimal("0.30")).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )

    now = int(datetime.now(timezone.utc).timestamp())
    created_time = int((datetime.now(timezone.utc) - timedelta(seconds=random.randint(1, 10))).timestamp())

    payment_intent_id = f"pi_{uuid.uuid4().hex[:24]}"
    charge_id = f"ch_{uuid.uuid4().hex[:24]}"

    payload = {
        "id": f"evt_{uuid.uuid4().hex}",
        "object": "event",
        "type": event_type,
        "created": now,
        "data": {
            "object": {
                "id": payment_intent_id,
                "object": "payment_intent",
                "status": status,
                "amount": money_cents(total),
                "currency": "usd",
                "created": created_time,
                "metadata": {
                    "order_id": f"order_{random.randint(10000, 99999)}",
                    "customer_name": name
                },
                "charges": {
                    "data": [
                        {
                            "id": charge_id,
                            "object": "charge",
                            "amount": money_cents(total),
                            "currency": "usd",
                            "status": status.lower(),
                            "paid": status == "COMPLETED",
                            "refunded": status == "REFUNDED",
                            "failure_message": reason if status == "FAILED" else None,
                            "receipt_email": f"user{random.randint(1,1000)}@example.com",
                            "created": created_time
                        }
                    ]
                },
                "application_fee_amount": money_cents(fee)
            }
        }
    }

    if status == "FAILED":
        payload["data"]["object"]["charges"]["data"][0]["outcome"] = {
            "reason": reason
        }

    return payload
