"""
Simplified sentiment analyzer (mocked, deterministic output).
"""
from typing import Dict
import hashlib


class SentimentAnalyzer:
    def get_sentiment(self, symbol: str) -> Dict:
        symbol = symbol.upper()
        seed = int(hashlib.sha256(symbol.encode("utf-8")).hexdigest(), 16)

        # Deterministic sentiment in range [-1, 1]
        sentiment_score = ((seed % 200) - 100) / 100.0

        # Confidence in range [0.6, 0.9]
        confidence = 0.6 + ((seed % 30) / 100.0)

        # Mentions in range [100, 1099]
        volume_mentions = 100 + (seed % 1000)

        return {
            "symbol": symbol,
            "sentiment_score": round(sentiment_score, 2),
            "confidence": round(confidence, 2),
            "volume_mentions": volume_mentions,
            "source": "mocked"
        }
