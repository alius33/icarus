"""FastAPI dependencies for JWT authentication."""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError

from app.auth.jwt_utils import decode_access_token
from app.config import settings

_bearer_scheme = HTTPBearer(auto_error=True)
_bearer_scheme_optional = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer_scheme),
) -> dict:
    """Mandatory auth dependency.

    Extracts the Bearer token, decodes it, and returns the payload.
    Raises 401 if the token is missing, invalid, or expired.
    """
    if not settings.AUTH_ENABLED:
        return {"sub": "anonymous", "auth_disabled": True}

    token = credentials.credentials
    try:
        payload = decode_access_token(token)
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    username: str | None = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing subject claim",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload


async def optional_auth(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme_optional),
) -> dict | None:
    """Optional auth dependency.

    Returns the decoded payload when a valid token is present, or ``None``
    when no Authorization header is provided.  Still raises 401 if a token
    IS provided but is invalid.
    """
    if not settings.AUTH_ENABLED:
        return None

    if credentials is None:
        return None

    token = credentials.credentials
    try:
        payload = decode_access_token(token)
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    return payload
