@echo off
echo Starting OmniVision AI Server...
echo.

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Run migrations
echo Running migrations...
python manage.py migrate

REM Create superuser if not exists
echo Creating superuser...
python manage.py create_superuser

REM Start the server
echo Starting Django server...
echo.
echo ========================================
echo OmniVision AI - Production Ready!
echo ========================================
echo.
echo 🚀 ACCESS POINTS:
echo ========================================
echo Main Dashboard: http://127.0.0.1:8000/api/core/ui/
echo Admin Interface: http://127.0.0.1:8000/admin/
echo API Documentation: http://127.0.0.1:8000/api/docs/
echo Login Page: http://127.0.0.1:8000/accounts/login/
echo.
echo 🔐 CREDENTIALS:
echo ========================================
echo Username: admin
echo Password: admin123
echo.
echo 📊 FEATURES:
echo ========================================
echo ✅ Multi-tab Industrial Dashboard
echo ✅ Worker Registration with Liveness Detection
echo ✅ Vehicle Registration with Commercial Options
echo ✅ Camera Management System
echo ✅ Real-time Monitoring & Alerts
echo ✅ Professional Industrial UI Theme
echo ✅ JWT Authentication & API Security
echo ✅ WebSocket Live Camera Feeds
echo.
echo ========================================
echo.
echo To start Celery worker (in a separate terminal):
echo celery -A OmniVisionAI worker -l info
echo.
echo To start Celery beat (in a separate terminal):
echo celery -A OmniVisionAI beat -l info
echo.
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver
