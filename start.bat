@echo off
cd /d "%~dp0backend"

echo ================================================
echo   Phone Inspection RAG System - Starting...
echo ================================================

echo [1/4] Installing dependencies...
pip install -r requirements.txt --upgrade --quiet

echo [2/4] Checking imports...
python -c "import fastapi; import uvicorn; import requests; import numpy; print('[OK] All imports ready')"
if %errorlevel% neq 0 (
    echo [FAIL] Import error. Trying to reinstall...
    pip install fastapi uvicorn requests numpy --upgrade --quiet
    python -c "import fastapi; import uvicorn; import requests; import numpy; print('[OK] All imports ready')"
    if %errorlevel% neq 0 (
        echo [FAIL] Please run manually: pip install -r requirements.txt
        pause
        exit /b 1
    )
)

echo [3/4] Indexing knowledge base (if needed)...
if not exist "vector_store\data.json" (
    python scripts/index_kb.py
    if %errorlevel% neq 0 (
        pause
        exit /b 1
    )
) else (
    echo [SKIP] Vector store already exists.
)

echo [4/4] Starting server...
start python main.py
echo.
echo Server starting at: http://localhost:8000
echo.
echo Waiting 5 seconds...
ping 127.0.0.1 -n 5 >nul

start http://localhost:8000/static/index.html

echo.
echo ================================================
echo  Server is running. Press Ctrl+C to stop,
echo  or close this window.
echo ================================================
echo.

:loop
ping 127.0.0.1 -n 10 >nul
goto loop
