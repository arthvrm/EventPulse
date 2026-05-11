import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from app.backend.main import app
from app.backend.etc.security import verify_hmac_signature
import json


class TestWebhookAPI:

    def test_webhook_paypal_success(self, client, sample_paypal_payload):
        # Generate signature
        secret = "supersecret"
        payload_bytes = json.dumps(sample_paypal_payload, separators=(',', ':')).encode()
        import hmac
        import hashlib
        signature = hmac.new(
            key=secret.encode(),
            msg=payload_bytes,
            digestmod=hashlib.sha256,
        ).hexdigest()

        response = client.post(
            "/webhook",
            content=payload_bytes,
            headers={"x-signature": signature}
        )

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_webhook_stripe_success(self, client, sample_stripe_payload):
        # Generate signature
        secret = "supersecret"
        payload_bytes = json.dumps(sample_stripe_payload, separators=(',', ':')).encode()
        import hmac
        import hashlib
        signature = hmac.new(
            key=secret.encode(),
            msg=payload_bytes,
            digestmod=hashlib.sha256,
        ).hexdigest()

        response = client.post(
            "/webhook",
            content=payload_bytes,
            headers={"x-signature": signature}
        )

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_webhook_invalid_signature(self, client, sample_paypal_payload):
        response = client.post(
            "/webhook",
            json=sample_paypal_payload,
            headers={"x-signature": "invalid"}
        )

        assert response.status_code == 401
        assert "Invalid signature" in response.json()["detail"]

    def test_webhook_missing_signature(self, client, sample_paypal_payload):
        response = client.post(
            "/webhook",
            json=sample_paypal_payload
        )

        assert response.status_code == 401
        assert "Invalid signature" in response.json()["detail"]

    def test_webhook_invalid_json(self, client):
        response = client.post(
            "/webhook",
            content=b'invalid json',
            headers={"x-signature": "dummy"}
        )

        assert response.status_code == 400
        assert "Invalid JSON payload" in response.json()["detail"]

    def test_webhook_unknown_provider(self, client):
        payload = {"unknown": "provider"}
        secret = "supersecret"
        payload_bytes = json.dumps(payload).encode()
        import hmac
        import hashlib
        signature = hmac.new(
            key=secret.encode(),
            msg=payload_bytes,
            digestmod=hashlib.sha256,
        ).hexdigest()

        response = client.post(
            "/webhook",
            content=payload_bytes,
            headers={"x-signature": signature}
        )

        assert response.status_code == 400
        assert "Unknown provider" in response.json()["detail"]