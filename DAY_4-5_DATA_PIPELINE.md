# DAYS 4-5: DATA COLLECTOR & MARKET DATA PIPELINE

## 📊 OVERVIEW

Days 4-5 focus on building the data ingestion layer—the critical pipeline that feeds real market data, sentiment data, and user trading data into your system.

---

## DAY 4: DATA COLLECTOR IMPLEMENTATION

### Objective
Create `data_collector.py` - async data pipeline for market data and sentiment analysis

### Architecture

```
┌─────────────────────────────────────────────────────┐
│         Data Collector Module                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────────┐   ┌──────────────┐              │
│  │  Yahoo       │   │  Alpha       │              │
│  │  Finance     │   │  Vantage     │              │
│  └──────┬───────┘   └──────┬───────┘              │
│         │                   │                      │
│         └─────────┬─────────┘                      │
│                   │                                │
│          ┌────────▼────────┐                       │
│          │ MarketDataCache │                       │
│          │ (Redis)         │                       │
│          └────────┬────────┘                       │
│                   │                                │
│         ┌─────────┴─────────┐                      │
│         │                   │                      │
│    ┌────▼────┐         ┌────▼─────┐              │
│    │ TimescaleDB      │  Analytics │              │
│    │ (History)        │ (Current)  │              │
│    └──────────┘       └────────────┘              │
│                                                     │
│  ┌──────────────┐   ┌──────────────┐              │
│  │ Sentiment    │   │ News & Social│              │
│  │ Analysis     │   │ Media API    │              │
│  └──────────────┘   └──────────────┘              │
└─────────────────────────────────────────────────────┘
```

### Implementation Tasks

#### Task 1: Data Collector Class Structure
```python
# backend/data_collector.py

import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from database import MarketData, SentimentData, engine

class DataCollector:
    def __init__(self):
        self.market_data_api = MarketDataAPI()
        self.sentiment_api = SentimentAnalysisAPI()
        self.cache = MarketDataCache()
        
    async def collect_market_data(self, symbols: List[str], period: str = "1d"):
        """
        Collect OHLCV data for symbols
        
        Args:
            symbols: List of stock tickers ["AAPL", "MSFT", "GOOGL"]
            period: "1d" (daily), "1h" (hourly), "5m" (5-min)
        
        Returns:
            DataFrame with columns: date, open, high, low, close, volume
        """
        # Implementation
        pass
    
    async def collect_sentiment_data(self, symbols: List[str]):
        """
        Collect sentiment scores from news, Twitter, Reddit
        
        Returns:
            Sentiment scores 0-1, news sentiment, social media mentions
        """
        # Implementation
        pass
    
    async def stream_real_time_prices(self, symbols: List[str], callback):
        """
        Stream real-time price updates via WebSocket
        
        Calls callback function when prices update
        """
        # Implementation
        pass
```

#### Task 2: Market Data API Integration
```python
# Data source 1: Yahoo Finance (free, no API key)
class YahooFinanceAPI:
    async def get_ohlcv(self, symbol: str, start_date, end_date):
        """
        Get historical OHLCV data from Yahoo Finance
        
        Example response:
        {
            "Date": ["2024-01-01", "2024-01-02", ...],
            "Open": [150.0, 151.5, ...],
            "High": [152.0, 153.0, ...],
            "Low": [149.5, 150.5, ...],
            "Close": [151.5, 152.5, ...],
            "Volume": [1000000, 950000, ...]
        }
        """
        # Use yfinance library
        pass

# Data source 2: Alpha Vantage (paid, requires API key)
class AlphaVantageAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"
    
    async def get_intraday(self, symbol: str, interval: str = "5min"):
        """
        Get intraday data (real-time trading data)
        
        Intervals: 1min, 5min, 15min, 30min, 60min
        """
        # Implementation
        pass
    
    async def get_technical_indicators(self, symbol: str):
        """
        Calculate RSI, MACD, Moving Averages
        """
        # Implementation
        pass
```

#### Task 3: Sentiment Analysis Pipeline
```python
# backend/sentiment_analyzer.py

class SentimentAnalysisAPI:
    async def analyze_news_sentiment(self, symbol: str):
        """
        Analyze financial news sentiment
        
        Sources:
        - Finnhub API
        - Newsapi.org
        - Seeking Alpha
        
        Returns:
            {
                "positive_news": 5,
                "negative_news": 2,
                "neutral_news": 3,
                "overall_sentiment": 0.65,  # 0-1 scale
                "news_items": [...]
            }
        """
        pass
    
    async def analyze_social_media(self, symbol: str):
        """
        Analyze social media sentiment
        
        Sources:
        - Twitter/X API
        - Reddit (r/stocks, r/investing)
        - StockTwits
        
        Returns:
            {
                "twitter_sentiment": 0.60,
                "reddit_sentiment": 0.55,
                "stocktwits_sentiment": 0.70,
                "volume": 10000,
                "trending": True
            }
        """
        pass
```

#### Task 4: Cache Layer (Redis)
```python
# backend/data_cache.py

class MarketDataCache:
    def __init__(self, redis_client):
        self.redis = redis_client
    
    async def get_latest_price(self, symbol: str):
        """
        Get cached latest price
        Cache expiry: 5 minutes for real-time
        """
        cache_key = f"price:{symbol}"
        cached = await self.redis.get(cache_key)
        return cached
    
    async def cache_ohlcv_data(self, symbol: str, data: pd.DataFrame):
        """
        Cache historical data
        Cache expiry: 24 hours
        """
        cache_key = f"ohlcv:{symbol}"
        await self.redis.set(cache_key, data.to_json(), ex=86400)
    
    async def get_sentiment_cache(self, symbol: str):
        """
        Get cached sentiment
        Cache expiry: 1 hour
        """
        pass
```

#### Task 5: Database Storage
```python
# Store market data in TimescaleDB (optimized for time-series)

async def store_market_data(session: Session, data: pd.DataFrame):
    """
    Store OHLCV data in TimescaleDB
    
    MarketData model:
    - id: Integer
    - symbol: String (ticker)
    - timestamp: DateTime
    - open: Float
    - high: Float
    - low: Float
    - close: Float
    - volume: Integer
    - vwap: Float (volume-weighted avg price)
    """
    for idx, row in data.iterrows():
        market_data = MarketData(
            symbol=row['symbol'],
            timestamp=row['date'],
            open=row['open'],
            high=row['high'],
            low=row['low'],
            close=row['close'],
            volume=row['volume']
        )
        session.add(market_data)
    
    await session.commit()

async def store_sentiment_data(session: Session, sentiment_dict: Dict):
    """
    Store sentiment analysis results
    
    SentimentData model:
    - id: Integer
    - symbol: String
    - timestamp: DateTime
    - news_sentiment: Float (-1 to 1)
    - social_sentiment: Float (-1 to 1)
    - overall_sentiment: Float (-1 to 1)
    - source: String (news, twitter, reddit)
    """
    sentiment_data = SentimentData(
        symbol=sentiment_dict['symbol'],
        timestamp=datetime.now(),
        news_sentiment=sentiment_dict.get('news_sentiment', 0),
        social_sentiment=sentiment_dict.get('social_sentiment', 0),
        overall_sentiment=sentiment_dict.get('overall_sentiment', 0)
    )
    session.add(sentiment_data)
    await session.commit()
```

#### Task 6: Async Data Pipelines
```python
# Continuously collect data in background

async def market_data_pipeline(symbols: List[str]):
    """
    Runs continuously, collecting data every 5 minutes
    """
    collector = DataCollector()
    
    while True:
        try:
            # Collect latest data
            data = await collector.collect_market_data(symbols)
            
            # Store in database
            async with SessionLocal() as session:
                await store_market_data(session, data)
            
            # Cache in Redis
            for symbol in symbols:
                symbol_data = data[data['symbol'] == symbol]
                await collector.cache.cache_ohlcv_data(symbol, symbol_data)
            
            logger.info(f"Collected data for {len(symbols)} symbols")
            
        except Exception as e:
            logger.error(f"Market data collection failed: {e}")
        
        # Wait 5 minutes before next collection
        await asyncio.sleep(300)

async def sentiment_pipeline(symbols: List[str]):
    """
    Runs continuously, analyzing sentiment every hour
    """
    collector = DataCollector()
    
    while True:
        try:
            # Collect sentiment
            sentiments = await asyncio.gather(
                *[collector.collect_sentiment_data(symbol) for symbol in symbols]
            )
            
            # Store in database
            async with SessionLocal() as session:
                for sentiment in sentiments:
                    await store_sentiment_data(session, sentiment)
            
            logger.info(f"Analyzed sentiment for {len(symbols)} symbols")
            
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
        
        # Wait 1 hour before next analysis
        await asyncio.sleep(3600)

# Run both pipelines concurrently
async def start_data_collection():
    symbols = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN"]
    
    await asyncio.gather(
        market_data_pipeline(symbols),
        sentiment_pipeline(symbols)
    )
```

#### Task 7: API Endpoints for Data Access
```python
# Add to main.py

@app.get("/api/market-data/{symbol}")
async def get_market_data(
    symbol: str,
    days: int = 30,
    session: Session = Depends(get_db)
):
    """
    Get historical market data for symbol
    
    Returns: OHLCV data for last N days
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    data = session.query(MarketData).filter(
        (MarketData.symbol == symbol.upper()) &
        (MarketData.timestamp >= start_date) &
        (MarketData.timestamp <= end_date)
    ).all()
    
    return {
        "symbol": symbol,
        "data": [
            {
                "date": d.timestamp.isoformat(),
                "open": d.open,
                "high": d.high,
                "low": d.low,
                "close": d.close,
                "volume": d.volume
            }
            for d in data
        ]
    }

@app.get("/api/sentiment/{symbol}")
async def get_sentiment(
    symbol: str,
    hours: int = 24,
    session: Session = Depends(get_db)
):
    """
    Get sentiment analysis for symbol
    
    Returns: Sentiment scores and news items
    """
    start_time = datetime.now() - timedelta(hours=hours)
    
    sentiments = session.query(SentimentData).filter(
        (SentimentData.symbol == symbol.upper()) &
        (SentimentData.timestamp >= start_time)
    ).all()
    
    return {
        "symbol": symbol,
        "sentiments": [
            {
                "timestamp": s.timestamp.isoformat(),
                "news_sentiment": s.news_sentiment,
                "social_sentiment": s.social_sentiment,
                "overall": s.overall_sentiment
            }
            for s in sentiments
        ]
    }
```

### Day 4 Deliverables
- [ ] `backend/data_collector.py` (400 lines)
- [ ] `backend/data_cache.py` (150 lines)
- [ ] `backend/sentiment_analyzer.py` (300 lines)
- [ ] Updated `main.py` with 2 new endpoints
- [ ] Updated `requirements.txt` with data APIs
- [ ] Database migration scripts for TimescaleDB
- [ ] Error handling and logging

---

## DAY 5: DATA PIPELINE TESTING & OPTIMIZATION

### Objective
Test data collection, optimize queries, implement monitoring

### Task 1: Unit Tests for Data Collector
```python
# backend/tests/test_data_collector.py

import pytest
from unittest.mock import Mock, patch, AsyncMock
from data_collector import DataCollector

@pytest.mark.asyncio
async def test_collect_market_data():
    """Test market data collection"""
    collector = DataCollector()
    
    data = await collector.collect_market_data(["AAPL", "MSFT"])
    
    assert len(data) > 0
    assert "AAPL" in data['symbol'].values
    assert all(col in data.columns for col in ['open', 'high', 'low', 'close', 'volume'])

@pytest.mark.asyncio
async def test_collect_sentiment_data():
    """Test sentiment collection"""
    collector = DataCollector()
    
    sentiment = await collector.collect_sentiment_data("AAPL")
    
    assert "overall_sentiment" in sentiment
    assert 0 <= sentiment['overall_sentiment'] <= 1

@pytest.mark.asyncio
async def test_cache_performance():
    """Test cache reduces API calls"""
    collector = DataCollector()
    
    # First call hits API
    data1 = await collector.collect_market_data(["AAPL"])
    
    # Second call should be cached
    with patch.object(collector.market_data_api, 'get_ohlcv') as mock_api:
        data2 = await collector.collect_market_data(["AAPL"])
        
        # API should not be called again
        mock_api.assert_not_called()
```

### Task 2: Integration Tests
```python
# backend/tests/test_data_integration.py

@pytest.mark.asyncio
async def test_full_pipeline():
    """Test complete data collection -> cache -> database flow"""
    async with AsyncSession(engine) as session:
        collector = DataCollector()
        
        # Collect data
        data = await collector.collect_market_data(["AAPL"])
        
        # Store in database
        await store_market_data(session, data)
        
        # Retrieve from database
        result = session.query(MarketData).filter(
            MarketData.symbol == "AAPL"
        ).first()
        
        assert result is not None
        assert result.symbol == "AAPL"
        assert result.close > 0
```

### Task 3: Performance Optimization
```python
# Optimize database queries with indexes

# backend/migrations/create_market_data_indexes.py

from alembic import op
import sqlalchemy as sa

def upgrade():
    # Create indexes for common queries
    op.create_index('idx_market_data_symbol_timestamp', 'market_data',
                    ['symbol', 'timestamp'], unique=False)
    op.create_index('idx_sentiment_data_symbol_timestamp', 'sentiment_data',
                    ['symbol', 'timestamp'], unique=False)
    op.create_index('idx_behavioral_event_user_date', 'behavioral_events',
                    ['user_id', 'event_date'], unique=False)

def downgrade():
    op.drop_index('idx_market_data_symbol_timestamp')
    op.drop_index('idx_sentiment_data_symbol_timestamp')
    op.drop_index('idx_behavioral_event_user_date')
```

### Task 4: Monitoring & Alerts
```python
# backend/monitoring.py

from prometheus_client import Counter, Gauge, Histogram
import time

# Define metrics
data_collection_duration = Histogram(
    'data_collection_seconds',
    'Time taken to collect market data',
    buckets=(1, 5, 10, 30, 60)
)

api_calls_total = Counter(
    'api_calls_total',
    'Total API calls',
    ['api_name', 'status']
)

data_freshness = Gauge(
    'data_freshness_seconds',
    'Time since last data update',
    ['symbol']
)

database_query_duration = Histogram(
    'database_query_seconds',
    'Time taken for database queries',
    buckets=(0.01, 0.05, 0.1, 0.5, 1)
)

# Use in code
@data_collection_duration.time()
async def collect_market_data(symbols):
    try:
        data = await DataCollector().collect_market_data(symbols)
        api_calls_total.labels(api_name='yahoo_finance', status='success').inc()
        return data
    except Exception as e:
        api_calls_total.labels(api_name='yahoo_finance', status='error').inc()
        raise
```

### Task 5: Error Handling & Retries
```python
# Implement exponential backoff for API calls

async def call_api_with_retry(api_func, max_retries=3, backoff_factor=2):
    """
    Call API with exponential backoff retry logic
    
    Retry on: Timeout, Rate Limit, Service Unavailable
    Don't retry on: Invalid parameter, Authentication error
    """
    for attempt in range(max_retries):
        try:
            return await api_func()
        
        except RateLimitError as e:
            if attempt < max_retries - 1:
                wait_time = backoff_factor ** attempt
                logger.warning(f"Rate limited, waiting {wait_time}s")
                await asyncio.sleep(wait_time)
            else:
                raise
        
        except (TimeoutError, ConnectionError) as e:
            if attempt < max_retries - 1:
                wait_time = backoff_factor ** attempt
                logger.warning(f"Connection error, retrying in {wait_time}s")
                await asyncio.sleep(wait_time)
            else:
                raise
        
        except AuthenticationError as e:
            logger.error(f"Authentication failed: {e}")
            raise  # Don't retry auth errors
```

### Task 6: Data Quality Validation
```python
# backend/data_validation.py

def validate_market_data(data: pd.DataFrame) -> bool:
    """
    Validate market data quality
    
    Checks:
    - No missing values
    - Price ranges reasonable (OHLC order)
    - Volume positive
    - Timestamps in order
    """
    
    # Check no NaN values
    if data.isnull().any().any():
        logger.error("Data contains NaN values")
        return False
    
    # Check OHLC order (Low <= Open,Close <= High)
    invalid = data[
        (data['low'] > data['open']) |
        (data['low'] > data['close']) |
        (data['high'] < data['open']) |
        (data['high'] < data['close'])
    ]
    if len(invalid) > 0:
        logger.error(f"Invalid OHLC values in {len(invalid)} rows")
        return False
    
    # Check volume positive
    if (data['volume'] < 0).any():
        logger.error("Negative volume detected")
        return False
    
    # Check price ranges (no stock price changes >50% in 1 day for real stocks)
    data['price_change_pct'] = (data['close'] - data['open']) / data['open'] * 100
    if (data['price_change_pct'].abs() > 50).any():
        logger.warning("Unusually large price changes detected (possible data error)")
    
    logger.info(f"Data validation passed: {len(data)} rows")
    return True
```

### Day 5 Deliverables
- [ ] `backend/tests/test_data_collector.py` (250 lines)
- [ ] `backend/tests/test_data_integration.py` (150 lines)
- [ ] Database migration scripts with indexes
- [ ] `backend/monitoring.py` (100 lines)
- [ ] `backend/data_validation.py` (150 lines)
- [ ] Performance benchmarks and optimization report
- [ ] Error handling improvements
- [ ] API endpoint tests

---

## SUMMARY: Days 4-5

### What You'll Have Built:
1. ✅ Real-time market data collection from multiple sources
2. ✅ Sentiment analysis pipeline (news + social media)
3. ✅ Redis caching layer for performance
4. ✅ TimescaleDB storage for time-series data
5. ✅ 4 new API endpoints for data access
6. ✅ Comprehensive test suite
7. ✅ Monitoring and alerting
8. ✅ Error handling with retries
9. ✅ Data quality validation

### System Capabilities:
- Collect data for 100+ symbols simultaneously
- Process sentiment from 10,000+ news items/day
- Cache 1 million price points
- <100ms response time for cached data
- 99.9% uptime for data pipeline

### Files to Create:
```
backend/
├── data_collector.py          (400 lines)
├── data_cache.py              (150 lines)
├── sentiment_analyzer.py       (300 lines)
├── data_validation.py         (150 lines)
├── monitoring.py              (100 lines)
├── tests/
│   ├── test_data_collector.py (250 lines)
│   ├── test_data_integration.py (150 lines)
└── migrations/
    └── create_indexes.py      (50 lines)
```

### Next: Day 6-7 Optimization Enhancement
- Refine portfolio optimization algorithms with real market data
- Backtest against historical data
- Validate behavioral adjustments improve returns
- Optimize for computational efficiency

---

*CONFIDENTIAL - Property of Zetheta Algorithms Private Limited*
