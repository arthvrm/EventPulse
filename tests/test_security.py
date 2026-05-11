import pytest
from app.backend.etc.security import verify_hmac_signature


class TestHMACSecurity:
    def test_verify_hmac_valid_signature(self):
        secret = "supersecret"
        payload = b'{"test": "data"}'
        import hmac
        import hashlib
        expected_signature = hmac.new(
            key=secret.encode(),
            msg=payload,
            digestmod=hashlib.sha256,
        ).hexdigest()

        result = verify_hmac_signature(secret, payload, expected_signature)
        assert result is True

    def test_verify_hmac_invalid_signature(self):
        secret = "supersecret"
        payload = b'{"test": "data"}'
        invalid_signature = "invalid_signature"

        result = verify_hmac_signature(secret, payload, invalid_signature)
        assert result is False

    def test_verify_hmac_missing_signature(self):
        secret = "supersecret"
        payload = b'{"test": "data"}'

        result = verify_hmac_signature(secret, payload, "")
        assert result is False

    def test_verify_hmac_wrong_secret(self):
        secret = "supersecret"
        wrong_secret = "wrongsecret"
        payload = b'{"test": "data"}'

        import hmac
        import hashlib
        wrong_signature = hmac.new(
            key=wrong_secret.encode(),
            msg=payload,
            digestmod=hashlib.sha256,
        ).hexdigest()

        result = verify_hmac_signature(secret, payload, wrong_signature)
        assert result is False

    def test_verify_hmac_different_payload(self):
        secret = "supersecret"
        payload = b'{"test": "data"}'
        different_payload = b'{"test": "different"}'

        import hmac
        import hashlib
        signature_for_different = hmac.new(
            key=secret.encode(),
            msg=different_payload,
            digestmod=hashlib.sha256,
        ).hexdigest()

        result = verify_hmac_signature(secret, payload, signature_for_different)
        assert result is False