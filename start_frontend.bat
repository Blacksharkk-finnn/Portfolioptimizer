@echo off
echo ====================================
echo Starting Behavioral Portfolio Frontend
echo ====================================

cd frontend

echo Installing Node dependencies...
call npm install --silent

echo.
echo Starting React development server...
call npm run dev
