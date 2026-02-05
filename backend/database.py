"""
Database configuration and models for Behavioral Portfolio Optimizer
"""
from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, JSON, TIMESTAMP, ForeignKey, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import uuid
import os

# Database URL (SQLite for demo, PostgreSQL for production)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./behavioral_portfolio.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class UserProfile(Base):
    """User profiles with behavioral characteristics"""
    __tablename__ = "user_profiles"

    user_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    
    # Risk profile
    risk_tolerance = Column(Float, default=0.5)  # 0-1 scale
    loss_aversion_coefficient = Column(Float, default=2.25)  # Kahneman-Tversky
    overconfidence_score = Column(Float, default=0.5)  # 0-1 scale
    
    # User characteristics
    experience_years = Column(Integer, default=0)
    investment_objective = Column(String(50))  # 'conservative', 'balanced', 'aggressive'
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    portfolios = relationship("Portfolio", back_populates="user")
    behavioral_events = relationship("BehavioralEvent", back_populates="user")


class Portfolio(Base):
    """User portfolio holdings"""
    __tablename__ = "portfolios"

    portfolio_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("user_profiles.user_id"), nullable=False)
    
    name = Column(String(100), default="Main Portfolio")
    total_value = Column(Float, default=0)
    cash_balance = Column(Float, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("UserProfile", back_populates="portfolios")
    positions = relationship("Position", back_populates="portfolio")
    recommendations = relationship("Recommendation", back_populates="portfolio")
    backtest_results = relationship("BacktestResult", back_populates="portfolio")


class Position(Base):
    """Individual security positions"""
    __tablename__ = "positions"

    position_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    portfolio_id = Column(String(36), ForeignKey("portfolios.portfolio_id"), nullable=False)
    
    symbol = Column(String(10), nullable=False)
    quantity = Column(Float, nullable=False)
    cost_basis = Column(Float, nullable=False)
    current_value = Column(Float, default=0)
    weight = Column(Float, default=0)  # Portfolio weight %
    
    entry_price = Column(Float)
    entry_date = Column(DateTime)
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    portfolio = relationship("Portfolio", back_populates="positions")


class BehavioralEvent(Base):
    """Detected behavioral events during trading"""
    __tablename__ = "behavioral_events"

    event_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("user_profiles.user_id"), nullable=False)
    
    event_type = Column(String(50), nullable=False)  # 'panic_sell', 'fomo_buy', 'loss_aversion', etc.
    severity = Column(Float)  # 0-1 scale
    confidence = Column(Float)  # Prediction confidence
    
    context = Column(JSON)  # Additional context data
    
    detected_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("UserProfile", back_populates="behavioral_events")


class BiasScore(Base):
    """Historical bias scoring for users"""
    __tablename__ = "bias_scores"

    score_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("user_profiles.user_id"), nullable=False)
    
    # Individual bias scores (0-100 scale)
    confirmation_bias = Column(Float, default=0)
    recency_bias = Column(Float, default=0)
    anchoring_bias = Column(Float, default=0)
    herding_behavior = Column(Float, default=0)
    loss_aversion = Column(Float, default=0)
    overconfidence = Column(Float, default=0)
    disposition_effect = Column(Float, default=0)
    regret_aversion = Column(Float, default=0)
    
    # Composite score
    overall_bias_score = Column(Float, default=0)
    
    calculated_at = Column(DateTime, default=datetime.utcnow)


class Recommendation(Base):
    """Portfolio optimization recommendations"""
    __tablename__ = "recommendations"

    recommendation_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    portfolio_id = Column(String(36), ForeignKey("portfolios.portfolio_id"), nullable=False)
    
    optimization_type = Column(String(50))  # 'mvo', 'black_litterman', 'risk_parity', 'behavioral'
    
    # Current vs Recommended
    current_allocation = Column(JSON)  # {symbol: weight}
    recommended_allocation = Column(JSON)  # {symbol: weight}
    
    # Expected metrics
    expected_return = Column(Float)
    expected_risk = Column(Float)
    expected_sharpe = Column(Float)
    
    # Behavioral adjustments made
    behavioral_adjustments = Column(JSON)
    
    rationale = Column(String(1000))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    accepted = Column(String(50))  # 'pending', 'accepted', 'rejected'

    # Relationships
    portfolio = relationship("Portfolio", back_populates="recommendations")


class BacktestResult(Base):
    """Historical backtesting results"""
    __tablename__ = "backtest_results"

    backtest_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    portfolio_id = Column(String(36), ForeignKey("portfolios.portfolio_id"), nullable=False)
    
    strategy_name = Column(String(100))
    
    # Period
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    
    # Performance metrics
    total_return = Column(Float)
    annual_return = Column(Float)
    volatility = Column(Float)
    sharpe_ratio = Column(Float)
    sortino_ratio = Column(Float)
    max_drawdown = Column(Float)
    calmar_ratio = Column(Float)
    
    # Behavioral score
    behavioral_score = Column(Float)
    
    detailed_results = Column(JSON)  # Additional metrics
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    portfolio = relationship("Portfolio", back_populates="backtest_results")


class MarketData(Base):
    """Time-series market data (TimescaleDB hypertable)"""
    __tablename__ = "market_data"

    market_data_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    time = Column(TIMESTAMP, nullable=False)
    symbol = Column(String(10), nullable=False)
    
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    adjusted_close = Column(Float)
    volume = Column(BigInteger)


class SentimentData(Base):
    """Sentiment analysis data"""
    __tablename__ = "sentiment_data"

    sentiment_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    time = Column(TIMESTAMP, nullable=False)
    symbol = Column(String(10))
    source = Column(String(50))  # 'news', 'twitter', 'reddit', 'analyst'
    
    sentiment_score = Column(Float)  # -1 to 1
    confidence = Column(Float)
    volume_mentions = Column(Integer)
    influential_score = Column(Float)


def get_db():
    """Dependency injection for database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database and create tables"""
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")
