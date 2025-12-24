# Run the FastAPI development server
# This script starts the backend API with hot reload enabled

Write-Host "🚀 Starting AI Surrogate Backend API..." -ForegroundColor Green
Write-Host ""

# Check if virtual environment is activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "⚠️  Virtual environment not activated!" -ForegroundColor Yellow
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    .\venv\Scripts\Activate.ps1
}

Write-Host "📍 API will be available at:" -ForegroundColor Cyan
Write-Host "   - Swagger UI: http://localhost:8000/docs" -ForegroundColor White
Write-Host "   - ReDoc: http://localhost:8000/redoc" -ForegroundColor White
Write-Host "   - API Root: http://localhost:8000" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""

# Run uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
