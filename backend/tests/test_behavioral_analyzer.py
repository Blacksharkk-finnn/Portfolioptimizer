"""
Tests for behavioral analyzer
"""
import pytest
from behavioral_analyzer import BehavioralAnalyzer


def test_disposition_effect():
    """Test disposition effect detection"""
    analyzer = BehavioralAnalyzer()
    trades = [
        {"action": "SELL", "symbol": "AAPL", "quantity": 10, "price": 150, "pnl": 100, "holding_days": 5},
        {"action": "SELL", "symbol": "MSFT", "quantity": 5, "price": 300, "pnl": -50, "holding_days": 30}
    ]
    score = analyzer._detect_disposition_effect(trades)
    assert 0 <= score <= 1


def test_loss_aversion():
    """Test loss aversion detection"""
    analyzer = BehavioralAnalyzer()
    trades = [
        {"action": "SELL", "pnl": 100, "holding_days": 5},
        {"action": "SELL", "pnl": -100, "holding_days": 50}
    ]
    score = analyzer._detect_loss_aversion(trades)
    assert 0 <= score <= 1


def test_overconfidence():
    """Test overconfidence detection"""
    analyzer = BehavioralAnalyzer()
    trades = [{"action": "BUY"} for _ in range(50)]
    score = analyzer._detect_overconfidence(trades, portfolio_value=100000)
    assert 0 <= score <= 1
