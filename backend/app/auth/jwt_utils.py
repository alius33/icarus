"""JWT token creation and decoding utilities."""

from datetime import UTC, datetime, timedelta
from typing import Any

from jose import jwt

from app.auth.config import ALGORITHM, SECRET_KEY, TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    """Create a signed JWT access token.

    Parameters
    ----------
    data:
        Payload claims to encode (typically ``{"sub": username}``).
    expires_delta:
        Custom expiration offset.  Falls back to ``TOKEN_EXPIRE_MINUTES``.

    Returns
    -------
    str
        Encoded JWT string.
    """
    to_encode = data.copy()
    expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=TOKEN_EXPIRE_MINUTES))
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any]:
    """Decode and validate a JWT access token.

    Parameters
    ----------
    token:
        The raw JWT string from the Authorization header.

    Returns
    -------
    dict
        Decoded payload.

    Raises
    ------
    JWTError
        If the token is invalid or expired.
    """
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
