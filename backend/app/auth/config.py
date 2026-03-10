"""Auth-specific configuration loaded from environment variables."""

import json
import os

SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production")
ALGORITHM: str = "HS256"
TOKEN_EXPIRE_MINUTES: int = int(os.getenv("TOKEN_EXPIRE_MINUTES", "480"))

# AUTH_USERS is a JSON dict of username:password_hash pairs.
# For development the fallback provides admin:admin (plain-text comparison
# when passlib is not available or hash is not bcrypt-formatted).
_raw_users = os.getenv("AUTH_USERS", "")


def get_auth_users() -> dict[str, str]:
    """Return the configured username -> password_hash mapping."""
    if _raw_users:
        try:
            return json.loads(_raw_users)
        except json.JSONDecodeError:
            pass
    # Default development credentials (plain-text, NOT for production)
    return {"admin": "admin"}
