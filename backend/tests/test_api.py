"""
Tests for API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    """Test health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["confidential"] == True


def test_market_data():
    """Test market data endpoint"""
    response = client.get("/api/market-data/AAPL")
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "AAPL"
    assert "data" in data


def test_sentiment():
    """Test sentiment endpoint"""
    response = client.get("/api/sentiment/AAPL")
    assert response.status_code == 200
    data = response.json()
    assert "sentiment_score" in data
    assert "confidence" in data


def test_backtest():
    """Test backtest endpoint"""
    returns = [0.01, -0.02, 0.015, 0.02, -0.01]
    response = client.post("/api/backtest/run", json=returns)
    assert response.status_code == 200
    data = response.json()
    assert "sharpe_ratio" in data
    assert "max_drawdown" in data
