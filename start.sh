#!/bin/bash

echo "========================================"
echo "Legacy Code Archaeologist - Quick Start"
echo "========================================"
echo ""

echo "[1/2] Starting Backend Server..."
cd backend
source venv/bin/activate
uvicorn main:app --reload &
BACKEND_PID=$!

echo "Waiting for backend to initialize..."
sleep 3

echo ""
echo "[2/2] Starting Frontend Server..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "========================================"
echo "Servers are running!"
echo "========================================"
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all servers..."

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
