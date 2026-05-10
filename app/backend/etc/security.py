import hmac
import hashlib
import logging
from pathlib import Path


logger = logging.getLogger(str(Path(__name__)))

def verify_hmac_signature(
    secret: str,
    payload: bytes,
    signature: str,
) -> bool:
    try:
        if not signature:
            raise ValueError("Missing X-Signature header")
        
        if not isinstance(signature, str):
            raise TypeError("X-Signature must be a string")

        computed = hmac.new(
            key=secret.encode(),
            msg=payload,
            digestmod=hashlib.sha256,
        ).hexdigest()

        return hmac.compare_digest(computed, signature)

    except Exception as e:
        logger.warning(f"HMAC verification failed. warning: {e}", exc_info=e)
        return False
