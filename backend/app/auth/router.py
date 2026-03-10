"""Authentication endpoints (login / token)."""

from fastapi import APIRouter, HTTPException, status
from passlib.hash import bcrypt
from pydantic import BaseModel

from app.auth.config import get_auth_users
from app.auth.jwt_utils import create_access_token

router = APIRouter(tags=["auth"])


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


def _verify_password(plain: str, stored: str) -> bool:
    """Verify a password against a stored value.

    Supports both bcrypt hashes (starting with ``$2b$``) and plain-text
    comparison for the default development credentials.
    """
    if stored.startswith("$2b$") or stored.startswith("$2a$"):
        return bcrypt.verify(plain, stored)
    # Plain-text fallback (development only)
    return plain == stored


@router.post("/auth/login", response_model=TokenResponse)
async def login(body: LoginRequest) -> TokenResponse:
    """Authenticate with username/password and receive a JWT token.

    In development (AUTH_ENABLED=False) this still works but the token is
    not required on protected endpoints.
    """
    users = get_auth_users()
    stored_password = users.get(body.username)

    if stored_password is None or not _verify_password(body.password, stored_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(data={"sub": body.username})
    return TokenResponse(access_token=token)
