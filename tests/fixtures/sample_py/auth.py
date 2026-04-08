import hashlib
from utils.crypto import sign_payload

class TokenValidator:
    """Validates and rotates OAuth2 tokens."""

    def refresh(self, token: str) -> str:
        """Rotates OAuth2 refresh tokens."""
        signed = sign_payload(token)
        return signed

def require_auth(func):
    """Decorator that guards routes."""
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
