from __future__ import annotations

import threading
import time
from dataclasses import dataclass


@dataclass(frozen=True)
class RateLimitResult:
    allowed: bool
    retry_after_seconds: int


class RateLimitError(RuntimeError):
    """Raised when a rate-limited action is attempted too soon."""

    def __init__(self, retry_after_seconds: int, message: str | None = None):
        self.retry_after_seconds = retry_after_seconds
        super().__init__(message or f"Rate limited. Retry after {retry_after_seconds}s.")


class RateLimiter:
    """
    Simple thread-safe cooldown rate limiter.

    Allows an action at most once per `min_interval_seconds`.
    Uses time.monotonic() so it is resilient to system clock changes.
    """

    def __init__(self, min_interval_seconds: int = 15):
        if min_interval_seconds <= 0:
            raise ValueError("min_interval_seconds must be > 0")

        self._min_interval = float(min_interval_seconds)
        self._lock = threading.RLock()
        self._last_allowed_at: float = 0.0  # monotonic seconds

    @property
    def min_interval_seconds(self) -> int:
        return int(self._min_interval)

    def check(self) -> RateLimitResult:
        """
        Check if an action is allowed right now without consuming the allowance.
        """
        now = time.monotonic()
        with self._lock:
            elapsed = now - self._last_allowed_at
            if elapsed >= self._min_interval:
                return RateLimitResult(allowed=True, retry_after_seconds=0)

            retry = int((self._min_interval - elapsed) + 0.999)  # ceil-ish
            return RateLimitResult(allowed=False, retry_after_seconds=retry)

    def allow(self) -> RateLimitResult:
        """
        Atomically check and consume the allowance.
        If allowed, updates internal timestamp.
        """
        now = time.monotonic()
        with self._lock:
            elapsed = now - self._last_allowed_at
            if elapsed >= self._min_interval:
                self._last_allowed_at = now
                return RateLimitResult(allowed=True, retry_after_seconds=0)

            retry = int((self._min_interval - elapsed) + 0.999)  # ceil-ish
            return RateLimitResult(allowed=False, retry_after_seconds=retry)

    def enforce(self) -> None:
        """
        Like allow(), but raises RateLimitError if not allowed.
        """
        res = self.allow()
        if not res.allowed:
            raise RateLimitError(res.retry_after_seconds)

    def reset(self) -> None:
        """
        Reset limiter so the next action is allowed immediately.
        """
        with self._lock:
            self._last_allowed_at = 0.0
