"""Simple in-memory rate limiting middleware for FastAPI."""

import time
from collections.abc import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

# Per-IP tracking: {ip: (request_count, window_start_timestamp)}
_read_buckets: dict[str, tuple[int, float]] = {}
_write_buckets: dict[str, tuple[int, float]] = {}

# Defaults
READ_LIMIT = 100  # requests per window
WRITE_LIMIT = 30  # requests per window
WINDOW_SECONDS = 60


def _is_write_method(method: str) -> bool:
    return method in ("POST", "PATCH", "PUT", "DELETE")


def _check_rate(
    buckets: dict[str, tuple[int, float]],
    ip: str,
    limit: int,
    now: float,
) -> tuple[bool, int]:
    """Check and update the rate-limit bucket for *ip*.

    Returns ``(allowed, remaining)`` where *allowed* is False when the
    limit has been exceeded.
    """
    count, window_start = buckets.get(ip, (0, now))

    # Reset window if it has elapsed
    if now - window_start >= WINDOW_SECONDS:
        buckets[ip] = (1, now)
        return True, limit - 1

    if count >= limit:
        return False, 0

    buckets[ip] = (count + 1, window_start)
    return True, limit - count - 1


class RateLimiterMiddleware(BaseHTTPMiddleware):
    """Lightweight per-IP rate limiter.

    * GET/HEAD/OPTIONS: up to ``READ_LIMIT`` per minute.
    * POST/PATCH/PUT/DELETE: up to ``WRITE_LIMIT`` per minute.

    Returns 429 when the limit is exceeded.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Determine client IP (trust X-Forwarded-For in typical proxy setups)
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            client_ip = forwarded.split(",")[0].strip()
        else:
            client_ip = request.client.host if request.client else "unknown"

        now = time.time()
        method = request.method.upper()

        if _is_write_method(method):
            allowed, remaining = _check_rate(_write_buckets, client_ip, WRITE_LIMIT, now)
            limit = WRITE_LIMIT
        else:
            allowed, remaining = _check_rate(_read_buckets, client_ip, READ_LIMIT, now)
            limit = READ_LIMIT

        if not allowed:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests. Please try again later."},
                headers={
                    "Retry-After": str(WINDOW_SECONDS),
                    "X-RateLimit-Limit": str(limit),
                    "X-RateLimit-Remaining": "0",
                },
            )

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(limit)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        return response
