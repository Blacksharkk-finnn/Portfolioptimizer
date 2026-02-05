"""
Behavioral Portfolio Optimization Engine
Implements bias-adjusted Modern Portfolio Theory and other optimization methods
"""
from typing import Dict, List, Tuple, Optional
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import norm


class BehavioralPortfolioOptimizer:
    """
    Portfolio optimization with behavioral adjustments
    Incorporates investor psychology into allocation decisions
    """

    def __init__(self, user_profile: Dict):
        """
        Initialize optimizer with user's behavioral profile
        
        Args:
            user_profile: Dict containing risk tolerance, loss aversion, etc.
        """
        self.risk_tolerance = user_profile.get('risk_tolerance', 0.5)
        self.loss_aversion = user_profile.get('loss_aversion_coefficient', 2.25)
        self.overconfidence = user_profile.get('overconfidence_score', 0.5)
        self.experience_years = user_profile.get('experience_years', 0)
        self.investment_objective = user_profile.get('investment_objective', 'balanced')

    def optimize_portfolio(
        self,
        expected_returns: np.ndarray,
        cov_matrix: np.ndarray,
        constraints: Optional[Dict] = None,
        method: str = 'behavioral_mvo'
    ) -> Dict:
        """
        Optimize portfolio with behavioral adjustments
        
        Args:
            expected_returns: Expected returns for each asset
            cov_matrix: Covariance matrix
            constraints: Dict of constraints (min_weight, max_weight, etc.)
            method: Optimization method ('behavioral_mvo', 'black_litterman', 'risk_parity')
        
        Returns:
            Dict with optimal weights, expected return, risk, etc.
        """

        if constraints is None:
            constraints = {
                'min_weight': 0.01,
                'max_weight': 0.30,
                'min_positions': 5
            }

        if method == 'behavioral_mvo':
            return self._behavioral_mean_variance_optimization(
                expected_returns, cov_matrix, constraints
            )
        elif method == 'black_litterman':
            return self._black_litterman_optimization(
                expected_returns, cov_matrix, constraints
            )
        elif method == 'risk_parity':
            return self._risk_parity_optimization(cov_matrix, constraints)
        else:
            raise ValueError(f"Unknown optimization method: {method}")

    def _behavioral_mean_variance_optimization(
        self,
        expected_returns: np.ndarray,
        cov_matrix: np.ndarray,
        constraints: Dict
    ) -> Dict:
        """
        Behavioral-adjusted Markowitz optimization
        Incorporates:
        - Prospect theory utility function
        - Loss aversion coefficients
        - Overconfidence adjustments
        - Mental accounting constraints
        """

        n_assets = len(expected_returns)

        # Step 1: Adjust expected returns for behavioral biases
        adjusted_returns = self._apply_behavioral_adjustments_to_returns(
            expected_returns, expected_returns.mean()
        )

        # Step 2: Adjust covariance for perceived risk
        adjusted_cov = self._adjust_risk_perception(cov_matrix)

        # Step 3: Define objective function
        def objective(weights):
            # Portfolio return
            portfolio_return = np.dot(weights, adjusted_returns)

            # Portfolio variance
            portfolio_variance = np.dot(weights, np.dot(adjusted_cov, weights))

            # Prospect theory utility
            # For positive returns, concave (diminishing returns)
            # For negative returns, convex (increasing sensitivity)
            utility = portfolio_return
            if portfolio_return < 0:
                # Losses feel worse due to loss aversion
                utility = -self.loss_aversion * abs(portfolio_return)

            # Negative because we're minimizing
            return -utility + 0.5 * portfolio_variance

        # Step 4: Constraints
        bounds = [
            (constraints['min_weight'], constraints['max_weight'])
            for _ in range(n_assets)
        ]

        # Sum to 1 constraint
        constraints_scipy = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}

        # Minimum number of positions constraint
        min_positions = constraints['min_positions']
        min_positions_constraint = {
            'type': 'ineq',
            'fun': lambda x: np.sum(x > 0.01) - min_positions + 1
        }

        # Step 5: Optimize
        initial_weights = np.ones(n_assets) / n_assets
        result = minimize(
            objective,
            initial_weights,
            method='SLSQP',
            bounds=bounds,
            constraints=[constraints_scipy, min_positions_constraint],
            options={'maxiter': 1000}
        )

        weights = np.maximum(result.x, 0)
        weights = weights / weights.sum()  # Renormalize

        # Calculate portfolio metrics
        expected_return = np.dot(weights, expected_returns)
        portfolio_variance = np.dot(weights, np.dot(cov_matrix, weights))
        portfolio_volatility = np.sqrt(portfolio_variance)
        sharpe_ratio = expected_return / portfolio_volatility if portfolio_volatility > 0 else 0

        return {
            'weights': weights,
            'expected_return': expected_return,
            'expected_volatility': portfolio_volatility,
            'sharpe_ratio': sharpe_ratio,
            'behavioral_adjustments': {
                'loss_aversion_coefficient': self.loss_aversion,
                'adjusted_returns_applied': True,
                'risk_perception_adjusted': True
            },
            'method': 'behavioral_mvo'
        }

    def _black_litterman_optimization(
        self,
        market_implied_returns: np.ndarray,
        cov_matrix: np.ndarray,
        constraints: Dict
    ) -> Dict:
        """
        Black-Litterman model with behavioral modifications
        Incorporates investor views with confidence levels
        """
        n_assets = len(market_implied_returns)

        # Risk aversion coefficient (behavioral adjustment)
        # Higher risk aversion for loss-averse investors
        risk_aversion = 2.5 / (1 + self.loss_aversion * 0.5)

        # Equilibrium returns (market weights * covariance * risk aversion)
        market_weights = np.ones(n_assets) / n_assets
        equilibrium_returns = risk_aversion * np.dot(cov_matrix, market_weights)

        # Confidence level in views (lower if overconfident)
        confidence = 0.5 / (1 + self.overconfidence)
        tau = confidence  # Uncertainty scalar

        # Combine equilibrium with views
        blended_returns = equilibrium_returns + tau * (market_implied_returns - equilibrium_returns)

        # Optimize with blended returns
        def objective(weights):
            portfolio_return = np.dot(weights, blended_returns)
            portfolio_variance = np.dot(weights, np.dot(cov_matrix, weights))
            return -portfolio_return + 0.5 * risk_aversion * portfolio_variance

        bounds = [
            (constraints['min_weight'], constraints['max_weight'])
            for _ in range(n_assets)
        ]

        constraints_scipy = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}

        initial_weights = np.ones(n_assets) / n_assets
        result = minimize(
            objective,
            initial_weights,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints_scipy,
            options={'maxiter': 1000}
        )

        weights = np.maximum(result.x, 0)
        weights = weights / weights.sum()

        expected_return = np.dot(weights, market_implied_returns)
        portfolio_variance = np.dot(weights, np.dot(cov_matrix, weights))
        portfolio_volatility = np.sqrt(portfolio_variance)

        return {
            'weights': weights,
            'expected_return': expected_return,
            'expected_volatility': portfolio_volatility,
            'sharpe_ratio': expected_return / portfolio_volatility if portfolio_volatility > 0 else 0,
            'method': 'black_litterman',
            'confidence_in_views': confidence
        }

    def _risk_parity_optimization(
        self,
        cov_matrix: np.ndarray,
        constraints: Dict
    ) -> Dict:
        """
        Risk Parity: Each asset contributes equally to portfolio risk
        Modified for behavioral preferences
        """
        n_assets = len(cov_matrix)

        def objective(weights):
            weights = np.maximum(weights, 0)
            if weights.sum() == 0:
                return 1e10

            weights = weights / weights.sum()

            # Risk contribution of each asset
            sigma = np.sqrt(np.diag(cov_matrix))
            marginal_contrib = np.dot(cov_matrix, weights)
            risk_contrib = weights * marginal_contrib

            # Target: each asset contributes equally
            target_contrib = np.sum(risk_contrib) / n_assets
            risk_diff = risk_contrib - target_contrib

            # Minimize squared differences
            return np.sum(risk_diff ** 2)

        bounds = [
            (constraints['min_weight'], constraints['max_weight'])
            for _ in range(n_assets)
        ]

        constraints_scipy = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}

        initial_weights = np.ones(n_assets) / n_assets
        result = minimize(
            objective,
            initial_weights,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints_scipy
        )

        weights = np.maximum(result.x, 0)
        weights = weights / weights.sum()

        # Calculate portfolio metrics
        portfolio_variance = np.dot(weights, np.dot(cov_matrix, weights))
        portfolio_volatility = np.sqrt(portfolio_variance)

        return {
            'weights': weights,
            'expected_volatility': portfolio_volatility,
            'method': 'risk_parity',
            'risk_contribution_equal': True
        }

    def _apply_behavioral_adjustments_to_returns(
        self,
        expected_returns: np.ndarray,
        reference_point: float
    ) -> np.ndarray:
        """
        Apply prospect theory value function to returns
        Adjusts for loss aversion and diminishing sensitivity
        """
        adjusted = np.zeros_like(expected_returns)

        for i, ret in enumerate(expected_returns):
            if ret >= reference_point:
                # Gain domain: concave (diminishing returns)
                # Exponent < 1 means diminishing sensitivity
                adjusted[i] = (ret - reference_point) ** 0.88
            else:
                # Loss domain: convex (increasing sensitivity)
                # Loss aversion coefficient applied
                adjusted[i] = -self.loss_aversion * (-(ret - reference_point)) ** 0.88

        return adjusted + reference_point

    def _adjust_risk_perception(self, cov_matrix: np.ndarray) -> np.ndarray:
        """
        Adjust covariance matrix for perceived risk
        Loss-averse investors perceive downside risk more strongly
        """
        adjusted_cov = cov_matrix.copy()

        # Extract diagonal (variances)
        variances = np.diag(adjusted_cov)

        # Amplify variances based on loss aversion
        adjustment_factor = 1 + (self.loss_aversion - 1) * 0.2

        adjusted_variances = variances * adjustment_factor
        np.fill_diagonal(adjusted_cov, adjusted_variances)

        return adjusted_cov

    def _apply_behavioral_constraints(
        self,
        weights: np.ndarray,
        constraints: Dict
    ) -> np.ndarray:
        """
        Apply behavioral guardrails to ensure psychological adherence
        """

        # Prevent over-concentration (overconfidence penalty)
        max_weight = constraints.get('max_weight', 0.30)
        max_weight_adjusted = max_weight / (1 + self.overconfidence * 0.5)
        weights = np.minimum(weights, max_weight_adjusted)

        # Ensure minimum diversification (loss aversion requirement)
        min_positions = constraints.get('min_positions', 5)
        num_positions = np.sum(weights > 0.01)

        if num_positions < min_positions:
            # Increase to minimum number of positions
            sorted_indices = np.argsort(-weights)
            for i in range(min_positions):
                weights[sorted_indices[i]] = max(weights[sorted_indices[i]], 0.05)

        # Normalize
        weights = weights / weights.sum()

        return weights


def calculate_portfolio_metrics(
    weights: np.ndarray,
    expected_returns: np.ndarray,
    cov_matrix: np.ndarray
) -> Dict:
    """
    Calculate comprehensive portfolio performance metrics
    """
    expected_return = np.dot(weights, expected_returns)
    variance = np.dot(weights, np.dot(cov_matrix, weights))
    volatility = np.sqrt(variance)

    # Calculate maximum drawdown (simplified)
    # In production, use historical data
    max_drawdown = volatility * 2  # Approximation

    # Sharpe ratio (assuming 2% risk-free rate)
    risk_free_rate = 0.02
    sharpe_ratio = (expected_return - risk_free_rate) / volatility if volatility > 0 else 0

    # Sortino ratio (downside deviation only)
    downside_variance = variance * 0.7  # Approximation
    downside_volatility = np.sqrt(downside_variance)
    sortino_ratio = (expected_return - risk_free_rate) / downside_volatility if downside_volatility > 0 else 0

    return {
        'expected_return': expected_return,
        'volatility': volatility,
        'sharpe_ratio': sharpe_ratio,
        'sortino_ratio': sortino_ratio,
        'max_drawdown': max_drawdown,
        'variance': variance
    }
