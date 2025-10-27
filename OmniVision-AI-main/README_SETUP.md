# 🚀 OmniVision AI - Complete Setup Guide

## ✅ Project Status: FULLY FIXED AND READY

All dashboard issues have been resolved:
- ✅ Logout works correctly
- ✅ No freezing or lag
- ✅ Independent camera management per tab
- ✅ Gate control with rename functionality
- ✅ All UI elements visible
- ✅ No duplicate functions
- ✅ Optimized performance

---

## 📥 Quick Setup (5 Minutes)

### Step 1: Install Dependencies
```bash
# Navigate to project
cd "OmniVision-AI-main\OmniVision-AI-main"

# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt
```

### Step 2: Setup Database
```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
# Enter: username (e.g., admin), email (optional), password
```

### Step 3: Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### Step 4: Start Redis (Required for Channels/Celery)
```bash
# Download Redis for Windows: https://github.com/microsoftarchive/redis/releases
# Or use WSL:
wsl
sudo apt-get install redis-server
redis-server
```

### Step 5: Run the Server
```bash
python manage.py runserver
```

### Step 6: Access the Application
Open browser: `http://127.0.0.1:8000/`

- Login: `http://127.0.0.1:8000/accounts/login/`
- Dashboard: `http://127.0.0.1:8000/api/core/ui/`
- Admin: `http://127.0.0.1:8000/admin/`

---

## 🎯 Features Working

### Dashboard Tab
- System metrics (Workers, PPE, Vehicles, Defects, Gates, Cameras)
- Gate control with lock/unlock/rename
- Live camera feeds (2×4 grid)
- System alerts

### Workers Tab
- Independent camera management
- Add cameras for attendance module
- View worker cameras in grid

### Vehicles Tab
- Independent camera management
- Add cameras for ANPR module
- Gate control integration
- View vehicle cameras

### PPE Tab
- Independent camera management
- Add cameras for PPE monitoring
- PPE-specific camera grid

### Textile Tab
- Independent camera management
- Add cameras for textile quality
- Textile-specific camera grid

### Settings Tab
- System configuration
- Settings panel

### Gate Features
- **Lock/Unlock**: Click button to toggle
- **Rename**: Click gate name to edit
- **Lock All**: One-click lock all gates
- **Unlock All**: One-click unlock all gates

### Camera Features
- **Add Camera**: Per-tab "Add Camera" button
- **Edit Camera**: Pencil icon on camera card
- **Delete Camera**: Trash icon on camera card
- **Module Assignment**: Auto-filled based on tab

---

## 📋 Required Packages

All listed in `requirements.txt`:
- django==5.2.6
- djangorestframework==3.16.1
- channels==4.3.1
- channels-redis==4.3.0
- celery==5.5.3
- redis==6.4.0
- ... and more

---

## 🐛 Troubleshooting

### Issue: ModuleNotFoundError
**Fix**: Make sure virtual environment is activated
```bash
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Issue: Redis connection error
**Fix**: Start Redis server
```bash
redis-server
# Or install: https://github.com/microsoftarchive/redis/releases
```

### Issue: Migration errors
**Fix**: Reset database
```bash
python manage.py flush
python manage.py makemigrations
python manage.py migrate
```

### Issue: Static files not loading
**Fix**: Recollect static files
```bash
python manage.py collectstatic --noinput
```

---

## 🎉 Success!

✅ **OmniVision AI Dashboard Successfully Fixed and Running.**

You can now:
1. Login at `http://127.0.0.1:8000/accounts/login/`
2. Access dashboard at `http://127.0.0.1:8000/api/core/ui/`
3. Add cameras for each tab independently
4. Control gates (lock/unlock/rename)
5. View live camera feeds
6. Monitor system metrics

**No further edits required. System is fully operational.**

