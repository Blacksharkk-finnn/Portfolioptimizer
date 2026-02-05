@echo off
echo ====================================
echo Starting Behavioral Portfolio Backend
echo ====================================

cd backend

echo Installing Python dependencies...
pip install fastapi uvicorn pydantic sqlalchemy yfinance pandas numpy scipy scikit-learn --quiet

echo.
echo Starting FastAPI server...
python main.py
