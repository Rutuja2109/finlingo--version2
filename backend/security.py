"""Abuse protection: rate limits for the sensitive endpoints, the real client address behind Render's proxy, and security headers.

The limiter is in memory (the server runs as one process), which is enough to stop password guessing and sign-up floods.
Set DISABLE_RATE_LIMIT=1 only for automated tests that create many accounts from one machine.
"""
import hashlib
import os
import time
from collections import deque

from fastapi import HTTPException, Request

TOO_MANY = "Too many attempts. Please wait a few minutes and try again."


def enabled() -> bool:
    return os.environ.get("DISABLE_RATE_LIMIT") != "1"


def client_ip(request: Request) -> str:
    """The caller's address. Behind Render's proxy it is the first X-Forwarded-For entry (without this, every visitor would
    look like Render's own proxy and share one limit). A determined caller could forge that header, so the per-address limits
    are generous and only a first line of defence; the strict limits are per account (login, reset), which cannot be dodged."""
    if os.environ.get("RENDER") or os.environ.get("TRUST_PROXY") == "1":
        fwd = request.headers.get("x-forwarded-for", "")
        if fwd:
            return fwd.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


class RateLimiter:
    def __init__(self):
        self._hits = {}
        self._gc_at = time.monotonic()

    def _recent(self, key: str, window: float, now: float) -> deque:
        q = self._hits.setdefault(key, deque())
        while q and q[0] <= now - window:
            q.popleft()
        return q

    def _gc(self, now: float):
        if now - self._gc_at < 300:
            return
        self._gc_at = now
        for k in [k for k, q in self._hits.items() if not q or q[-1] <= now - 86400]:
            self._hits.pop(k, None)

    def blocked(self, key: str, limit: int, window: float) -> float:
        """Seconds until the caller may try again, or 0 if they are within the limit."""
        now = time.monotonic()
        self._gc(now)
        q = self._recent(key, window, now)
        return max(0.0, q[0] + window - now) if len(q) >= limit else 0.0

    def hit(self, key: str, window: float):
        now = time.monotonic()
        self._recent(key, window, now).append(now)

    def clear(self, key: str):
        self._hits.pop(key, None)

    def reset_all(self):
        self._hits.clear()


limiter = RateLimiter()


def _refuse(wait: float):
    raise HTTPException(status_code=429, detail=TOO_MANY, headers={"Retry-After": str(int(wait) + 1)})


def enforce(request: Request, name: str, limit: int, window: float, who: str = None):
    """Count this call and refuse it with 429 once the caller has made `limit` calls in `window` seconds."""
    if not enabled():
        return
    key = f"{name}:{who or client_ip(request)}"
    wait = limiter.blocked(key, limit, window)
    if wait:
        _refuse(wait)
    limiter.hit(key, window)


def check_blocked(key: str, limit: int, window: float):
    """Refuse (429) if `key` already has `limit` recorded failures; does not count anything itself."""
    if not enabled():
        return
    wait = limiter.blocked(key, limit, window)
    if wait:
        _refuse(wait)


def record_failure(key: str, window: float):
    if enabled():
        limiter.hit(key, window)


def clear(key: str):
    limiter.clear(key)


def token_hash(token: str) -> str:
    """Reset links are stored only as a hash, so a database leak does not hand out working links."""
    return hashlib.sha256(token.encode()).hexdigest()


HTML_CSP = "default-src 'none'; style-src 'unsafe-inline'; img-src data:; form-action 'self'; base-uri 'none'; frame-ancestors 'none'"


def add_security_headers(response, is_html: bool = False):
    h = response.headers
    h["X-Content-Type-Options"] = "nosniff"
    h["Referrer-Policy"] = "no-referrer"
    h["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    if os.environ.get("RENDER") or os.environ.get("FORCE_HSTS") == "1":
        h["Strict-Transport-Security"] = "max-age=31536000"
    if is_html:
        h["X-Frame-Options"] = "DENY"
        h["Content-Security-Policy"] = HTML_CSP
        h["Cache-Control"] = "no-store"
    return response
