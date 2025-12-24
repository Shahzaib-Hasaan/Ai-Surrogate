@echo off
REM Run the FastAPI development server
REM This script starts the backend API with hot reload enabled

echo.
echo ========================================
echo   AI Surrogate Backend API
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run: python -m venv venv
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Starting FastAPI server...
echo.
echo API will be available at:
echo   - Swagger UI: http://localhost:8000/docs
echo   - ReDoc: http://localhost:8000/redoc
echo   - API Root: http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.
echo ========================================
echo.

REM Run uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
