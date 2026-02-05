# Quick Start Guide

## Prerequisites
- Python 3.10+
- Node.js 18+
- Docker Desktop (optional)

## Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Run the FastAPI server:
```bash
python main.py
```

API will be available at `http://localhost:8000`
API docs at `http://localhost:8000/docs`

## Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm run dev
```

Frontend will be available at `http://localhost:3000`

## Running Tests

Backend tests:
```bash
cd backend
pytest tests/ -v
```

## API Endpoints

- `GET /health` - Health check
- `GET /api/market-data/{symbol}` - Get market data
- `GET /api/sentiment/{symbol}` - Get sentiment analysis
- `POST /api/users/register` - Register user
- `POST /api/optimization/optimize` - Optimize portfolio
- `POST /api/bias/analyze` - Analyze behavioral biases
- `POST /api/backtest/run` - Run backtest

## Demo

The system demonstrates:
- Real-time market data visualization
- Sentiment analysis
- Behavioral bias detection (8 biases)
- Portfolio optimization with behavioral adjustments
- Backtesting capabilities

## Architecture

- **Backend**: FastAPI (Python)
- **Frontend**: React + Material-UI
- **Data**: yfinance for market data
- **Charts**: Recharts
- **Testing**: pytest

## Notes

This is a demonstration system. For production:
- Add proper authentication
- Use real-time data feeds
- Implement database persistence
- Add comprehensive error handling
- Deploy with Docker/Kubernetes
