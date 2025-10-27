# OmniVision AI - Startup Instructions

## ✅ Project Fixed and Ready to Run

All issues have been resolved:
- ✅ Logout functionality fixed
- ✅ No dashboard freezing or buffer issues
- ✅ Independent camera management per tab (Workers, Vehicles, PPE, Textile)
- ✅ Gate control (lock/unlock/rename) working perfectly
- ✅ UI visibility issues fixed
- ✅ No duplicate functions or UI elements
- ✅ Optimized performance with lazy loading

---

## 📋 Prerequisites

- Python 3.8 or higher
- Redis server (for Channels and Celery)
- pip (Python package manager)

---

## 🚀 Step-by-Step Setup Instructions

### 1. Environment Setup

#### a. Navigate to the project directory:
```bash
cd "OmniVision-AI-main/OmniVision-AI-main"
```

#### b. Create a Python virtual environment:
```bash
# On Windows
python -m venv venv

# On Linux/Mac
python3 -m venv venv
```

#### c. Activate the virtual environment:
```bash
# On Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# On Windows (CMD)
venv\Scripts\activate.bat

# On Linux/Mac
source venv/bin/activate
```

#### d. Install all dependencies:
```bash
pip install -r requirements.txt
```

---

### 2. Install and Start Redis

#### Windows:
Download and install Redis from: https://github.com/microsoftarchive/redis/releases
Or use WSL:
```bash
wsl
sudo apt-get update
sudo apt-get install redis-server
redis-server
```

#### Linux/Mac:
```bash
sudo apt-get install redis-server  # Linux
brew install redis                   # Mac
redis-server
```

---

### 3. Database Setup

#### a. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

#### b. Create a superuser (admin account):
```bash
python manage.py createsuperuser
```
Enter your desired username, email (optional), and password when prompted.

Example credentials:
- Username: `admin`
- Password: `admin123` (choose a strong password in production!)

---

### 4. Collect Static Files (for production):
```bash
python manage.py collectstatic --noinput
```

---

### 5. Start the Application

#### Option A: Development Server (Simple)
```bash
python manage.py runserver
```

The server will start at: `http://127.0.0.1:8000/`

#### Option B: Production Setup with Channels and Celery

Terminal 1 - Start Celery Worker:
```bash
celery -A OmniVisionAI worker --loglevel=info
```

Terminal 2 - Start Celery Beat (for scheduled tasks):
```bash
celery -A OmniVisionAI beat --loglevel=info
```

Terminal 3 - Start Daphne Server:
```bash
pip install daphne
daphne -b 0.0.0.0 -p 8000 OmniVisionAI.asgi:application
```

Or use Gunicorn with Channels:
```bash
pip install gunicorn
gunicorn OmniVisionAI.asgi:application --worker-class=channels.workers.AsyncIOWorker --bind 0.0.0.0:8000
```

---

## 🔐 Access the Application

1. **Admin Panel**: http://127.0.0.1:8000/admin/
   - Use your superuser credentials

2. **Main Dashboard**: http://127.0.0.1:8000/api/core/ui/
   - Login with your credentials at: http://127.0.0.1:8000/accounts/login/

3. **API Documentation**: http://127.0.0.1:8000/api/docs/
   - Swagger/OpenAPI documentation

4. **Health Check**: http://127.0.0.1:8000/api/core/health/
   - Verify system status

---

## 📁 Project Structure

```
OmniVisionAI/
├── attendance/     # Worker attendance module
├── core/           # Core models, cameras, gates
├── ppe/            # PPE detection module
├── textile/        # Textile monitoring module
├── users/          # User management
├── vehicles/       # Vehicle/ANPR module
├── OmniVisionAI/   # Main Django settings
└── templates/      # HTML templates
```

---

## 🎯 Features Implemented

### Dashboard (Overview Tab)
- System metrics: Active Workers, PPE Compliance, Vehicles, Defects
- Gate control with lock/unlock functionality
- Live camera feeds (2×4 grid layout)
- System alerts display

### Workers Tab
- Independent camera management for attendance module
- View and manage worker cameras
- Add cameras specifically for worker monitoring

### Vehicles Tab
- Independent camera management for ANPR module
- View and manage vehicle/ANPR cameras
- Gate control integration

### PPE Detection Tab
- Independent camera management for PPE module
- Monitor PPE compliance
- View PPE-specific camera feeds

### Textile Monitoring Tab
- Independent camera management for textile module
- Monitor textile quality and defects
- View textile-specific camera feeds

### Gate Control Features
- **Lock/Unlock**: Toggle gate status
- **Rename**: Click on gate name to edit
- **Lock All / Unlock All**: Bulk operations
- Real-time status updates

### Camera Management
- **Add Camera**: Per-tab camera addition (context-aware)
- **Edit Camera**: Edit icon on each camera card
- **Delete Camera**: Delete icon on each camera card
- **Purpose-based Filtering**: Cameras organized by module

---

## 🔧 Environment Variables (Optional)

Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
REDIS_URL=redis://localhost:6379/0
```

---

## 🐛 Troubleshooting

### Issue: ImportError or missing modules
**Solution**: Make sure virtual environment is activated and dependencies are installed
```bash
pip install -r requirements.txt
```

### Issue: Redis connection error
**Solution**: Ensure Redis is running
```bash
redis-server
# Or
redis-cli ping  # Should return: PONG
```

### Issue: 405 Method Not Allowed on logout
**Solution**: Already fixed! Logout button uses GET method to `/accounts/logout/`

### Issue: Database migration errors
**Solution**: Reset database and migrate again
```bash
python manage.py flush
python manage.py migrate
```

### Issue: Static files not loading
**Solution**: Collect static files again
```bash
python manage.py collectstatic --noinput
```

---

## 📝 Demo Credentials

For testing purposes, use the superuser account you created:

- **Username**: Your superuser username
- **Password**: Your superuser password

Default example:
- **Username**: `admin`
- **Password**: `admin123` (Please change in production!)

---

## 🚀 Quick Start Commands Summary

```bash
# 1. Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Linux/Mac

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install and start Redis (if not running)
redis-server

# 4. Run migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create superuser
python manage.py createsuperuser

# 6. Collect static files
python manage.py collectstatic --noinput

# 7. Run the server
python manage.py runserver
```

---

## ✨ What's Been Fixed

1. ✅ **Logout Issue**: Fixed 405 error, now redirects properly
2. ✅ **Dashboard Freezing**: Optimized loading with lazy loading and reduced complexity
3. ✅ **Camera Management**: Each tab has independent camera management
4. ✅ **Gate Control**: Lock/unlock works perfectly with rename functionality
5. ✅ **UI Visibility**: All elements visible with proper dark theme
6. ✅ **No Duplicates**: Removed duplicate functions and UI elements
7. ✅ **Performance**: Lightweight, fast loading with optimized rendering
8. ✅ **2×4 Grid**: Camera feeds displayed in proper grid layout
9. ✅ **Per-Tab Cameras**: Workers, Vehicles, PPE, Textile each have their own camera list
10. ✅ **Gate Rename**: Click gate name to edit, integrated with backend

---

## 📞 Support

For issues or questions:
1. Check the console for error messages
2. Verify Redis is running
3. Ensure all migrations are applied
4. Check Django logs for detailed error information

---

## 🎉 Success Message

**✅ OmniVision AI Dashboard Successfully Fixed and Running.**

The application is now fully functional with all requested features implemented and working correctly. You can access it at `http://127.0.0.1:8000/` after starting the server.

