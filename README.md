# Behavioral Portfolio Optimizer

An end-to-end behavioral finance demo that detects investor biases, analyzes market sentiment, and produces bias-aware portfolio optimization recommendations. The project includes a FastAPI backend, a React + Vite frontend, and a lightweight SQLite database for portability.

## Features

- Real-time market data (yfinance)
- Deterministic sentiment analysis (mocked)
- Behavioral bias scoring dashboard
- Portfolio optimization recommendations
- Backtesting metrics
- Polished, responsive UI

## Tech Stack

**Backend:** FastAPI, SQLAlchemy, SQLite, NumPy, Pandas, yfinance

**Frontend:** React 18, Vite, Material UI, Recharts

## Quickstart

### Backend

1) From the project root:

```
cd backend
python -m venv .venv
.
```

2) Install dependencies:

```
pip install -r requirements-minimal.txt
```

3) Start the API:

```
python main.py
```

API runs at http://127.0.0.1:8000

### Frontend

1) From the project root:

```
cd frontend
npm install --legacy-peer-deps
```

2) Start the UI:

```
npm run dev -- --host 0.0.0.0 --port 3000
```

Open http://127.0.0.1:3000

## Demo Endpoints

- GET /health
- GET /api/market-data/{symbol}
- GET /api/sentiment/{symbol}
- POST /api/optimization/optimize
- POST /api/backtest/run

## Notes

- SQLite is used for a zero-config demo.
- No external API keys required.
- If npm install fails, run `npm cache clean --force` and retry.

## License

MIT

*Last Updated: January 31, 2026*  
*Project Status: Initialization Phase*
