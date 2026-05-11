import pytest
from app.mock_provider.core.event_provider import EventProvider
from app.mock_provider.services.hmac_service import HMACService
from app.mock_provider.services.webhook_sender import WebhookSender
from app.mock_provider.event_generators.paypal import generate_payload as generate_paypal
from app.mock_provider.event_generators.stripe import generate_payload as generate_stripe


class TestHMACService:
    def test_sign_payload(self):
        service = HMACService("testsecret")
        payload = {"test": "data"}

        signature1 = service.sign(payload)
        signature2 = service.sign(payload)

        assert signature1 == signature2  # Deterministic
        assert isinstance(signature1, str)
        assert len(signature1) == 64  # SHA256 hex length

    def test_sign_different_payloads(self):
        service = HMACService("testsecret")
        payload1 = {"test": "data1"}
        payload2 = {"test": "data2"}

        signature1 = service.sign(payload1)
        signature2 = service.sign(payload2)

        assert signature1 != signature2


class TestWebhookSender:
    def test_sender_initialization(self):
        sender = WebhookSender("http://example.com/webhook")
        assert sender.url == "http://example.com/webhook"


class TestEventProvider:
    def test_provider_initialization(self):
        def dummy_generator():
            return {"test": "event"}

        provider = EventProvider(
            secret="testsecret",
            webhook_url="http://example.com/webhook",
            generator=dummy_generator
        )

        assert provider.hmac.secret == b"testsecret"
        assert provider.sender.url == "http://example.com/webhook"

    @pytest.mark.asyncio
    async def test_generate_event(self):
        def dummy_generator():
            return {"type": "test.event"}

        provider = EventProvider(
            secret="testsecret",
            webhook_url="http://example.com/webhook",
            generator=dummy_generator
        )

        event = await provider.generate_event()
        assert event == {"type": "test.event"}

    @pytest.mark.asyncio
    async def test_sign_event(self):
        def dummy_generator():
            return {"type": "test.event"}

        provider = EventProvider(
            secret="testsecret",
            webhook_url="http://example.com/webhook",
            generator=dummy_generator
        )

        event = {"type": "test.event"}
        signature = await provider.sign(event)

        assert isinstance(signature, str)
        assert len(signature) == 64


class TestPayPalGenerator:
    def test_generate_paypal_payload(self):
        payload = generate_paypal()

        assert "id" in payload
        assert "event_type" in payload
        assert "resource_type" in payload
        assert "resource" in payload
        assert payload["resource_type"] in ["checkout-order", "capture", "authorization"]

    def test_paypal_payload_structure(self):
        payload = generate_paypal()

        assert "resource" in payload
        resource = payload["resource"]
        assert "id" in resource
        assert "status" in resource
        assert "amount" in resource
        assert "currency_code" in resource["amount"]
        assert "value" in resource["amount"]


class TestStripeGenerator:
    def test_generate_stripe_payload(self):
        payload = generate_stripe()

        assert "id" in payload
        assert payload["object"] == "event"
        assert "type" in payload
        assert "data" in payload
        assert "object" in payload["data"]

    def test_stripe_payload_structure(self):
        payload = generate_stripe()

        data_object = payload["data"]["object"]
        assert "id" in data_object
        assert "status" in data_object
        assert "amount" in data_object
        assert "currency" in data_object
        assert "charges" in data_object