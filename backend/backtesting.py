"""
Simple backtesting module (minimal for demo).
"""
from dataclasses import dataclass
from typing import List, Dict
import numpy as np


@dataclass
class BacktestResult:
    total_return: float
    annual_return: float
    volatility: float
    sharpe_ratio: float
    max_drawdown: float


def run_backtest(returns: List[float], risk_free_rate: float = 0.02) -> BacktestResult:
    """
    Simple backtest calculation from returns series.
    """
    returns_arr = np.array(returns)
    
    # Total return
    total_return = np.prod(1 + returns_arr) - 1
    
    # Annualized return (assuming daily returns)
    n_periods = len(returns_arr)
    annual_return = (1 + total_return) ** (252 / n_periods) - 1
    
    # Volatility
    volatility = np.std(returns_arr) * np.sqrt(252)
    
    # Sharpe ratio
    excess_return = annual_return - risk_free_rate
    sharpe_ratio = excess_return / volatility if volatility > 0 else 0
    
    # Max drawdown
    cumulative = np.cumprod(1 + returns_arr)
    running_max = np.maximum.accumulate(cumulative)
    drawdown = (cumulative - running_max) / running_max
    max_drawdown = np.min(drawdown)
    
    return BacktestResult(
        total_return=float(total_return),
        annual_return=float(annual_return),
        volatility=float(volatility),
        sharpe_ratio=float(sharpe_ratio),
        max_drawdown=float(max_drawdown)
    )
