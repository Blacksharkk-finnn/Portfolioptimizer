"""
FastAPI Application for Behavioral Portfolio Optimizer
Main API server with endpoints for portfolio management and bias detection
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from typing import List, Dict, Optional
import uvicorn
from datetime import datetime
import asyncio
import traceback

# Import core modules
from database import UserProfile, Portfolio, Position, get_db, init_db
from behavioral_analyzer import BehavioralAnalyzer, detect_real_time_bias
from portfolio_optimizer import BehavioralPortfolioOptimizer, calculate_portfolio_metrics
from data_collector import DataCollector
from sentiment_analyzer import SentimentAnalyzer
from backtesting import run_backtest
import numpy as np
import pandas as pd

# Initialize FastAPI app
app = FastAPI(
    title="Behavioral Portfolio Optimizer API",
    description="CONFIDENTIAL - Zetheta Algorithms Private Limited",
    version="1.0.0"
)

# Initialize helpers
data_collector = DataCollector()
sentiment_analyzer = SentimentAnalyzer()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Request/Response Models
# ============================================================================

class UserProfileRequest(BaseModel):
    """User profile creation request"""
    email: EmailStr
    password: str
    risk_tolerance: float  # 0-1
    experience_years: int
    investment_objective: str  # 'conservative', 'balanced', 'aggressive'


class UserProfileResponse(BaseModel):
    """User profile response"""
    user_id: str
    email: str
    risk_tolerance: float
    loss_aversion_coefficient: float
    overconfidence_score: float
    experience_years: int
    investment_objective: str
    created_at: datetime


class TradeRequest(BaseModel):
    """Trade/transaction request"""
    portfolio_id: str
    symbol: str
    action: str  # 'BUY', 'SELL'
    quantity: float
    price: float
    trade_date: datetime


class OptimizationRequest(BaseModel):
    """Portfolio optimization request"""
    portfolio_id: str
    assets: List[str]
    method: str = "behavioral_mvo"
    constraints: Optional[Dict] = None


class OptimizationResponse(BaseModel):
    """Portfolio optimization response"""
    portfolio_id: str
    method: str
    weights: Dict[str, float]
    expected_return: float
    expected_volatility: float
    sharpe_ratio: float
    behavioral_adjustments: Dict


class BiasScoreResponse(BaseModel):
    """Behavioral bias scoring response"""
    user_id: str
    confirmation_bias: float
    recency_bias: float
    anchoring_bias: float
    herding_behavior: float
    loss_aversion: float
    overconfidence: float
    disposition_effect: float
    regret_aversion: float
    overall_bias_score: float


class BiasEventResponse(BaseModel):
    """Real-time behavioral event response"""
    event_type: str
    severity: float
    timestamp: datetime
    context: Dict


# ============================================================================
# Endpoints
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Behavioral Portfolio Optimizer",
        "version": "1.0.0",
        "confidential": True
    }


@app.post("/api/users/register", response_model=UserProfileResponse)
async def register_user(user_data: UserProfileRequest, db = Depends(get_db)):
    """
    Register a new user with behavioral profile
    """
    try:
        # Check if user exists
        existing_user = db.query(UserProfile).filter(
            UserProfile.email == user_data.email
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists"
            )

        # Create new user
        new_user = UserProfile(
            email=user_data.email,
            password_hash=user_data.password,  # In production, hash this!
            risk_tolerance=user_data.risk_tolerance,
            experience_years=user_data.experience_years,
            investment_objective=user_data.investment_objective,
            loss_aversion_coefficient=2.25,  # Default
            overconfidence_score=0.5  # Default
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return UserProfileResponse(
            user_id=str(new_user.user_id),
            email=new_user.email,
            risk_tolerance=new_user.risk_tolerance,
            loss_aversion_coefficient=new_user.loss_aversion_coefficient,
            overconfidence_score=new_user.overconfidence_score,
            experience_years=new_user.experience_years,
            investment_objective=new_user.investment_objective,
            created_at=new_user.created_at
        )

    except Exception as e:
        print("Optimization error:", e)
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.post("/api/optimization/optimize", response_model=OptimizationResponse)
async def optimize_portfolio(request: OptimizationRequest, db = Depends(get_db)):
    """
    Optimize portfolio with behavioral adjustments
    """
    try:
        # Get portfolio (optional - use defaults if not found for demo)
        portfolio = db.query(Portfolio).filter(
            Portfolio.portfolio_id == request.portfolio_id
        ).first()

        # Use defaults if portfolio doesn't exist (for demo)
        if portfolio:
            user = db.query(UserProfile).filter(
                UserProfile.user_id == portfolio.user_id
            ).first()
        else:
            user = None

        # User profile with defaults for demo
        user_profile_dict = {
            'risk_tolerance': user.risk_tolerance if user else 0.5,
            'loss_aversion_coefficient': user.loss_aversion_coefficient if user else 2.25,
            'overconfidence_score': user.overconfidence_score if user else 0.5,
            'experience_years': user.experience_years if user else 0,
            'investment_objective': user.investment_objective if user else 'balanced'
        }

        optimizer = BehavioralPortfolioOptimizer(user_profile_dict)

        # Mock market data
        n_assets = len(request.assets)
        np.random.seed(hash(request.portfolio_id) % 2**32)  # Deterministic for demo
        expected_returns = np.array([0.085, 0.095, 0.075])[:n_assets]
        cov_matrix = np.array([[0.04, 0.015, 0.010],
                               [0.015, 0.05, 0.012],
                               [0.010, 0.012, 0.035]])[:n_assets, :n_assets]

        # Ensure constraints are feasible for the number of assets
        constraints = request.constraints or {}
        if not isinstance(constraints, dict):
            constraints = {}

        min_weight = float(constraints.get('min_weight', 0.01))
        max_weight = float(constraints.get('max_weight', 0.30))
        min_positions = int(constraints.get('min_positions', n_assets))

        # Make sure max_weight allows weights to sum to 1
        if max_weight * n_assets < 1.0:
            max_weight = 1.0 / n_assets

        # Min positions cannot exceed number of assets
        if min_positions > n_assets:
            min_positions = n_assets

        constraints = {
            'min_weight': min_weight,
            'max_weight': max_weight,
            'min_positions': min_positions
        }

        # Run optimization
        result = optimizer.optimize_portfolio(
            expected_returns,
            cov_matrix,
            constraints=constraints,
            method=request.method
        )

        # Format weights
        weights_dict = {
            request.assets[i]: float(result['weights'][i])
            for i in range(len(request.assets))
        }

        return OptimizationResponse(
            portfolio_id=request.portfolio_id,
            method=result['method'],
            weights=weights_dict,
            expected_return=float(result['expected_return']),
            expected_volatility=float(result['expected_volatility']),
            sharpe_ratio=float(result['sharpe_ratio']),
            behavioral_adjustments=result['behavioral_adjustments']
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.post("/api/bias/analyze")
async def analyze_behavioral_biases(
    user_id: str,
    trades: List[Dict],
    db = Depends(get_db)
):
    """
    Analyze user's behavioral biases from trading history
    """
    try:
        # Get user
        user = db.query(UserProfile).filter(
            UserProfile.user_id == user_id
        ).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Analyze trades
        analyzer = BehavioralAnalyzer()
        bias_scores, behavioral_events = analyzer.analyze_user_trades(trades)

        # Update user profile with detected biases
        user.loss_aversion_coefficient = 2.25 + (bias_scores.loss_aversion * 0.5)
        user.overconfidence_score = bias_scores.overconfidence

        db.commit()

        # Format events
        events = [
            {
                'event_type': event.event_type,
                'severity': event.severity,
                'timestamp': event.timestamp,
                'context': event.context
            }
            for event in behavioral_events
        ]

        return {
            'user_id': user_id,
            'bias_scores': {
                'confirmation_bias': bias_scores.confirmation_bias,
                'recency_bias': bias_scores.recency_bias,
                'anchoring_bias': bias_scores.anchoring_bias,
                'herding_behavior': bias_scores.herding_behavior,
                'loss_aversion': bias_scores.loss_aversion,
                'overconfidence': bias_scores.overconfidence,
                'disposition_effect': bias_scores.disposition_effect,
                'regret_aversion': bias_scores.regret_aversion,
                'overall_bias_score': bias_scores.overall_score
            },
            'behavioral_events': events,
            'num_events_detected': len(behavioral_events),
            'analysis_timestamp': datetime.utcnow()
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.post("/api/bias/detect-trade-bias")
async def detect_trade_bias(trade: TradeRequest):
    """
    Real-time detection of behavioral bias during trade execution
    """
    try:
        # TODO: Get current market conditions
        market_conditions = {
            'market_down_percent': -2.5,
            'market_up_percent': 0,
            'sentiment_score': 0.3,
            'trading_volume': 100000000
        }

        event = detect_real_time_bias(
            current_trade={
                'action': trade.action,
                'symbol': trade.symbol,
                'last_price_change': -3.0  # Mock
            },
            user_profile={},
            market_conditions=market_conditions
        )

        if event:
            return {
                'bias_detected': True,
                'event_type': event.event_type,
                'severity': event.severity,
                'recommendation': f"⚠️ You may be exhibiting {event.event_type}. Consider waiting 5 minutes before executing.",
                'context': event.context
            }
        else:
            return {
                'bias_detected': False,
                'recommendation': "✓ Trade appears rationally motivated"
            }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.get("/api/portfolio/{portfolio_id}")
async def get_portfolio(portfolio_id: str, db = Depends(get_db)):
    """
    Get portfolio details and current holdings
    """
    try:
        portfolio = db.query(Portfolio).filter(
            Portfolio.portfolio_id == portfolio_id
        ).first()

        if not portfolio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Portfolio not found"
            )

        # Get positions
        positions = db.query(Position).filter(
            Position.portfolio_id == portfolio_id
        ).all()

        return {
            'portfolio_id': str(portfolio.portfolio_id),
            'name': portfolio.name,
            'total_value': portfolio.total_value,
            'cash_balance': portfolio.cash_balance,
            'positions': [
                {
                    'symbol': pos.symbol,
                    'quantity': pos.quantity,
                    'current_value': pos.current_value,
                    'weight': pos.weight,
                    'entry_price': pos.entry_price
                }
                for pos in positions
            ],
            'updated_at': portfolio.updated_at
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.get("/api/market-data/{symbol}")
async def get_market_data(symbol: str, period: str = "1mo", interval: str = "1d"):
    """
    Get recent market data for a symbol (via yfinance)
    """
    try:
        data = await asyncio.to_thread(
            data_collector.get_market_data,
            symbol,
            period,
            interval
        )
        return {
            "symbol": symbol.upper(),
            "period": period,
            "interval": interval,
            "source": "yfinance",
            "data": data
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.get("/api/sentiment/{symbol}")
async def get_sentiment(symbol: str):
    """
    Get sentiment data for a symbol (mocked, deterministic)
    """
    try:
        sentiment = sentiment_analyzer.get_sentiment(symbol)
        return sentiment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.post("/api/backtest/run")
async def run_backtest_endpoint(returns: List[float], risk_free_rate: float = 0.02):
    """
    Run simple backtest on returns series
    """
    try:
        result = run_backtest(returns, risk_free_rate)
        return {
            "total_return": result.total_return,
            "annual_return": result.annual_return,
            "volatility": result.volatility,
            "sharpe_ratio": result.sharpe_ratio,
            "max_drawdown": result.max_drawdown
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ============================================================================
# Startup/Shutdown Events
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    print("Starting Behavioral Portfolio Optimizer API...")
    print("CONFIDENTIAL - Property of Zetheta Algorithms Private Limited")
    init_db()
    print("Database initialized")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("Shutting down Behavioral Portfolio Optimizer API...")


# ============================================================================
# Error Handling
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "timestamp": datetime.utcnow(),
            "confidential": True
        }
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
