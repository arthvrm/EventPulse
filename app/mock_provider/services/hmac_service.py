import hmac
import hashlib
import json


class HMACService:
    def __init__(self, secret: str):
        self.secret = secret.encode()

    def sign(self, payload: dict) -> str:
        message = json.dumps(payload, separators=(",", ":")).encode()

        return hmac.new(
            self.secret,
            message,
            hashlib.sha256
        ).hexdigest()
