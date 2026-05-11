import random
from typing import Any, Dict
import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal, ROUND_HALF_UP

from app.mock_provider.event_generators.event_collections import (
    PAYPAL_EVENT_STATUS_MAP,
    PAYPAL_FAILURE_REASON_MAP,
    PAYPAL_RESOURCE_TYPE_MAP,
    PRODUCTS
)


def iso_z(dt: datetime) -> str:
    return dt.isoformat().replace("+00:00", "Z")

def money(value: Decimal) -> str:
    return str(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def generate_payload() -> Dict[str, Any]:
    event_type = random.choice(list(PAYPAL_EVENT_STATUS_MAP.keys()))
    status = PAYPAL_EVENT_STATUS_MAP[event_type]
    
    base_event = ".".join(event_type.split(".")[:2])
    resource_type = PAYPAL_RESOURCE_TYPE_MAP[base_event]
    
    now = datetime.now(timezone.utc)
    created_time = now - timedelta(seconds=random.randint(1, 10))

    selected_products = random.sample(PRODUCTS, k=random.randint(1, 3))
    
    items = []
    total = Decimal("0")
    
    if base_event == "CHECKOUT.ORDER":
        for product_name, category, price in selected_products:
            quantity = random.randint(1, 2)
            total += Decimal(str(price)) * quantity

            items.append({
                "name": product_name,
                "unit_amount": {
                    "currency_code": "USD",
                    "value": money(Decimal(str(price)))
                },
                "quantity": str(quantity),
                "category": category
            })
    elif base_event != "CHECKOUT.ORDER":
        total = Decimal(str(random.uniform(10, 200))).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

    fee = (total * Decimal("0.03"))
    fee = fee.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    
    net = (total - fee).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    
    resource_id_prefix = resource_type.lower()

    resource = {
        "id": f"{resource_id_prefix}-{uuid.uuid4().hex}",
        "status": status,
        "amount": {
            "currency_code": "USD",
            "value": money(Decimal(str(total)))
        },
        "create_time": iso_z(created_time),
        "update_time": iso_z(now),
        "custom_id": f"order_{random.randint(10000, 99999)}",
        "invoice_id": f"inv_{random.randint(10000, 99999)}",
        "payer": {
            "email_address": f"user{random.randint(1,1000)}@example.com",
            "payer_id": f"PAYER-{uuid.uuid4().hex[:10]}"
        }
    }
    
    if resource_type == "capture":
        resource["seller_receivable_breakdown"] = {
            "gross_amount": {
                "currency_code": "USD",
                "value": money(Decimal(str(total)))
            },
            "paypal_fee": {
                "currency_code": "USD",
                "value": money(Decimal(str(fee)))
            },
            "net_amount": {
                "currency_code": "USD",
                "value": money(Decimal(str(net)))
            }
        }
    
    if status in {"FAILED", "DENIED", "REVERSED", "VOIDED"}:
        resource["status_details"] = {
            "reason": random.choice(
                PAYPAL_FAILURE_REASON_MAP.get(event_type, ["NONE"])
            )
        }
    
    payload = {
        "id": f"WH-{uuid.uuid4().hex}",
        "event_type": event_type,
        "resource_type": resource_type,
        "create_time": iso_z(now),
        "resource": resource
    }

    return payload
