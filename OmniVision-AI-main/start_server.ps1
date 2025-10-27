Write-Host "Starting OmniVision AI Server..." -ForegroundColor Green
Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

# Run migrations
Write-Host "Running migrations..." -ForegroundColor Yellow
python manage.py migrate

# Create superuser if not exists
Write-Host "Creating superuser..." -ForegroundColor Yellow
python manage.py create_superuser

# Start the server
Write-Host "Starting Django server..." -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "OmniVision AI - Production Ready!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🚀 ACCESS POINTS:" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Main Dashboard: http://127.0.0.1:8000/api/core/ui/" -ForegroundColor White
Write-Host "Admin Interface: http://127.0.0.1:8000/admin/" -ForegroundColor White
Write-Host "API Documentation: http://127.0.0.1:8000/api/docs/" -ForegroundColor White
Write-Host "Login Page: http://127.0.0.1:8000/accounts/login/" -ForegroundColor White
Write-Host ""
Write-Host "🔐 CREDENTIALS:" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Username: admin" -ForegroundColor White
Write-Host "Password: admin123" -ForegroundColor White
Write-Host ""
Write-Host "📊 FEATURES:" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ Multi-tab Industrial Dashboard" -ForegroundColor Green
Write-Host "✅ Worker Registration with Liveness Detection" -ForegroundColor Green
Write-Host "✅ Vehicle Registration with Commercial Options" -ForegroundColor Green
Write-Host "✅ Camera Management System" -ForegroundColor Green
Write-Host "✅ Real-time Monitoring & Alerts" -ForegroundColor Green
Write-Host "✅ Professional Industrial UI Theme" -ForegroundColor Green
Write-Host "✅ JWT Authentication & API Security" -ForegroundColor Green
Write-Host "✅ WebSocket Live Camera Feeds" -ForegroundColor Green
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To start Celery worker (in a separate terminal):" -ForegroundColor Yellow
Write-Host "celery -A OmniVisionAI worker -l info" -ForegroundColor White
Write-Host ""
Write-Host "To start Celery beat (in a separate terminal):" -ForegroundColor Yellow
Write-Host "celery -A OmniVisionAI beat -l info" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Red
Write-Host ""

python manage.py runserver
