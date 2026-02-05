"""
Market data collection using yfinance (simplified for accelerated delivery).
"""
from typing import List, Dict, Any
import yfinance as yf
import pandas as pd

from data_cache import SimpleTTLCache


class DataCollector:
    def __init__(self, cache: SimpleTTLCache | None = None):
        self.cache = cache or SimpleTTLCache(ttl_seconds=300)

    def get_market_data(self, symbol: str, period: str = "1mo", interval: str = "1d") -> List[Dict[str, Any]]:
        cache_key = f"market:{symbol.upper()}:{period}:{interval}"
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached

        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period, interval=interval, auto_adjust=False)

        if df is None or df.empty:
            return []

        df = df.reset_index()
        time_col = None
        if "Date" in df.columns:
            time_col = "Date"
        elif "Datetime" in df.columns:
            time_col = "Datetime"
        else:
            time_col = df.columns[0]

        df = df.rename(
            columns={
                time_col: "time",
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Volume": "volume",
            }
        )

        records = []
        for _, row in df.iterrows():
            records.append(
                {
                    "time": pd.to_datetime(row["time"]).isoformat(),
                    "open": float(row.get("open", 0.0)) if pd.notna(row.get("open")) else None,
                    "high": float(row.get("high", 0.0)) if pd.notna(row.get("high")) else None,
                    "low": float(row.get("low", 0.0)) if pd.notna(row.get("low")) else None,
                    "close": float(row.get("close", 0.0)) if pd.notna(row.get("close")) else None,
                    "volume": float(row.get("volume", 0.0)) if pd.notna(row.get("volume")) else None,
                }
            )

        self.cache.set(cache_key, records, ttl_seconds=300)
        return records

    def get_latest_price(self, symbol: str) -> Dict[str, Any]:
        data = self.get_market_data(symbol, period="5d", interval="1d")
        if not data:
            return {
                "symbol": symbol.upper(),
                "price": None,
                "time": None,
            }
        latest = data[-1]
        return {
            "symbol": symbol.upper(),
            "price": latest.get("close"),
            "time": latest.get("time"),
        }
