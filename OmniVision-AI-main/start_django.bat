@echo off
echo ========================================
echo  OmniVision AI - Starting Server
echo ========================================
echo.

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Check if migrations are needed
echo Checking for pending migrations...
python manage.py showmigrations --list | findstr /C:"[ ]"

REM Run migrations
echo Running migrations...
python manage.py makemigrations --noinput
python manage.py migrate --noinput

REM Collect static files
echo Collecting static files...
python manage.py collectstatic --noinput

echo.
echo ========================================
echo  Starting Django Development Server
echo  Open browser: http://127.0.0.1:8000/
echo  Press Ctrl+C to stop the server
echo ========================================
echo.

REM Start the server
python manage.py runserver

