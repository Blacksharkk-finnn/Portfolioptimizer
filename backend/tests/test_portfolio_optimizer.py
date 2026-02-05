"""
Tests for portfolio optimizer
"""
import pytest
import numpy as np
from portfolio_optimizer import BehavioralPortfolioOptimizer


def test_behavioral_mvo():
    """Test behavioral mean-variance optimization"""
    user_profile = {
        'risk_tolerance': 0.7,
        'loss_aversion_coefficient': 2.25,
        'overconfidence_score': 0.5,
        'experience_years': 5,
        'investment_objective': 'balanced'
    }
    
    optimizer = BehavioralPortfolioOptimizer(user_profile)
    
    expected_returns = np.array([0.10, 0.12, 0.08, 0.15])
    cov_matrix = np.eye(4) * 0.05
    
    result = optimizer.optimize_portfolio(expected_returns, cov_matrix, method='behavioral_mvo')
    
    assert 'weights' in result
    assert 'sharpe_ratio' in result
    assert len(result['weights']) == 4
    assert np.isclose(np.sum(result['weights']), 1.0, atol=0.01)


def test_risk_parity():
    """Test risk parity optimization"""
    user_profile = {'risk_tolerance': 0.5}
    optimizer = BehavioralPortfolioOptimizer(user_profile)
    
    expected_returns = np.array([0.08, 0.10, 0.09])
    cov_matrix = np.eye(3) * 0.04
    
    result = optimizer.optimize_portfolio(expected_returns, cov_matrix, method='risk_parity')
    
    assert 'weights' in result
    assert len(result['weights']) == 3
