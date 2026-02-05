"""
Simple in-memory TTL cache for market data and sentiment.
Avoids external dependencies for accelerated delivery.
"""
from dataclasses import dataclass
from typing import Any, Dict, Optional
import time


@dataclass
class CacheItem:
    value: Any
    expires_at: float


class SimpleTTLCache:
    def __init__(self, ttl_seconds: int = 300):
        self.ttl_seconds = ttl_seconds
        self._store: Dict[str, CacheItem] = {}

    def get(self, key: str) -> Optional[Any]:
        item = self._store.get(key)
        if not item:
            return None
        if item.expires_at < time.time():
            self._store.pop(key, None)
            return None
        return item.value

    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        ttl = ttl_seconds if ttl_seconds is not None else self.ttl_seconds
        self._store[key] = CacheItem(value=value, expires_at=time.time() + ttl)
