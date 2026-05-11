import pytest
from datetime import datetime, timezone
from app.backend.normalizers.paypal import PayPalNormalizer
from app.backend.normalizers.stripe import StripeNormalizer


class TestPayPalNormalizer:
    def test_paypal_normalizer_completed_capture(self, sample_raw_event_paypal):
        normalizer = PayPalNormalizer()
        result = normalizer.normalize(sample_raw_event_paypal)

        assert result.provider == "paypal"
        assert result.payment_id == "capture-123"
        assert result.event_id == "WH-1234567890"
        assert result.event_type == "PAYMENT.CAPTURE.COMPLETED"
        assert result.status == "COMPLETED"
        assert result.amount == 100.00
        assert result.currency == "USD"
        assert result.fee == 3.00
        assert result.net_amount == 97.00
        assert result.order_id == "order-123"
        assert result.customer_id == "PAYER-123"
        assert result.latency_ms > 0

    def test_paypal_normalizer_failed_capture(self, sample_raw_event_paypal):
        # Modify payload to have failed status
        sample_raw_event_paypal.payload["resource"]["status"] = "FAILED"
        sample_raw_event_paypal.payload["resource"]["status_details"] = {"reason": "INSUFFICIENT_FUNDS"}

        normalizer = PayPalNormalizer()
        result = normalizer.normalize(sample_raw_event_paypal)

        assert result.status == "FAILED"
        assert result.failure_reason == "INSUFFICIENT_FUNDS"

    def test_paypal_normalizer_without_fee(self, sample_raw_event_paypal):
        # Remove seller_receivable_breakdown
        del sample_raw_event_paypal.payload["resource"]["seller_receivable_breakdown"]

        normalizer = PayPalNormalizer()
        result = normalizer.normalize(sample_raw_event_paypal)

        assert result.amount == 100.00
        assert result.fee is None
        assert result.net_amount is None


class TestStripeNormalizer:
    def test_stripe_normalizer_succeeded_payment(self, sample_raw_event_stripe):
        normalizer = StripeNormalizer()
        result = normalizer.normalize(sample_raw_event_stripe)

        assert result.provider == "stripe"
        assert result.payment_id == "pi_1234567890"
        assert result.event_id == "evt_1234567890"
        assert result.event_type == "payment_intent.succeeded"
        assert result.status == "succeeded"
        assert result.amount == 100.00  # Converted from cents
        assert result.currency == "USD"
        assert result.fee == 3.00  # Converted from cents
        assert result.net_amount == 97.00
        assert result.order_id == "order-123"
        assert result.customer_id == "test@example.com"
        assert result.latency_ms > 0

    def test_stripe_normalizer_failed_payment(self, sample_raw_event_stripe):
        # Modify payload to have failed status
        sample_raw_event_stripe.payload["data"]["object"]["status"] = "failed"
        sample_raw_event_stripe.payload["data"]["object"]["charges"]["data"][0]["failure_message"] = "card_declined"

        normalizer = StripeNormalizer()
        result = normalizer.normalize(sample_raw_event_stripe)

        assert result.status == "failed"
        assert result.failure_reason == "card_declined"

    def test_stripe_normalizer_refunded_payment(self, sample_raw_event_stripe):
        # Modify payload to have refunded status
        sample_raw_event_stripe.payload["type"] = "charge.refunded"
        sample_raw_event_stripe.payload["data"]["object"]["status"] = "refunded"

        normalizer = StripeNormalizer()
        result = normalizer.normalize(sample_raw_event_stripe)

        assert result.event_type == "charge.refunded"
        assert result.status == "refunded"