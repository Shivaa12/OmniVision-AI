# 🚀 OmniVision AI - Industrial Surveillance & Automation Dashboard

## 🎯 Overview

OmniVision AI is a comprehensive industrial-grade surveillance and automation system built with Django, featuring real-time monitoring, gate control, worker management, vehicle tracking, PPE compliance, and textile quality control. The system provides a unified dashboard for managing all aspects of industrial operations with professional UI/UX design.

## ✨ Key Features

### 🏭 **Industrial-Grade Dashboard**
- **Professional UI/UX**: Dark slate gray + industrial blue color scheme
- **Real-time Metrics**: Live statistics for workers, vehicles, PPE compliance, and system status
- **Responsive Design**: Optimized for desktop and tablet viewing
- **Smooth Animations**: GSAP-powered transitions and effects

### 🚪 **Gate Control System**
- **Real-time Gate Management**: Lock/unlock gates with live status updates
- **Bulk Operations**: Lock all gates, unlock all gates with single click
- **Access Logging**: Complete audit trail of gate access events
- **Visual Status Indicators**: Color-coded gate status (red=locked, green=unlocked)

### 👥 **Worker Management**
- **Comprehensive Registration**: Full worker profiles with emergency contacts
- **Liveness Detection**: Webcam-based face verification (left → right → center)
- **Face Recognition**: Store face embeddings for attendance tracking
- **Shift Management**: Multiple shift timings and department assignments

### 🚛 **Vehicle Management**
- **Vehicle Registration**: Complete vehicle profiles with owner information
- **Commercial Support**: Special handling for commercial vehicles and agencies
- **ANPR Integration**: Automatic number plate recognition for gate access
- **Authorization Tracking**: Real-time vehicle authorization status

### 📹 **Camera Management**
- **Multi-Camera Support**: IP, RTSP, HTTP, and USB camera integration
- **Live Feeds**: Real-time camera streaming with 2x4 grid layout
- **Purpose-Based Organization**: Cameras assigned to specific modules (PPE, Vehicle, Textile)
- **Camera Controls**: Add, edit, delete cameras with live preview

### 🛡️ **PPE Monitoring**
- **Real-time Compliance**: Live PPE violation detection
- **Camera Integration**: Dedicated PPE monitoring cameras
- **Compliance Tracking**: Percentage-based compliance monitoring

### 🧵 **Textile Quality Control**
- **Defect Detection**: AI-powered textile defect identification
- **Quality Monitoring**: Real-time quality control metrics
- **Camera Feeds**: Dedicated textile inspection cameras

## 🛠️ Technical Stack

### Backend
- **Django 5.2.6** - Web framework
- **Django REST Framework 3.16.1** - API development
- **Django Channels 4.3.1** - WebSocket support
- **Celery 5.5.3** - Background task processing
- **Redis 6.4.0** - Caching and message broker
- **PostgreSQL/SQLite** - Database

### Frontend
- **Bootstrap 5.3.3** - UI framework
- **Chart.js 4.4.1** - Data visualization
- **GSAP 3.12.2** - Animations
- **WebSocket API** - Real-time communication
- **Vanilla JavaScript** - Interactive functionality

### AI/ML
- **OpenCV** - Computer vision
- **MediaPipe** - Face detection
- **Dlib** - Face recognition
- **Custom Models** - PPE and textile defect detection

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Redis server
- Webcam (for liveness detection)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd OmniVision-AI-main
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser --username admin --email admin@example.com --noinput
   ```

6. **Start the system**
   ```bash
   # Terminal 1: Django server
   python manage.py runserver
   
   # Terminal 2: Celery worker
   celery -A OmniVisionAI worker -l info
   
   # Terminal 3: Celery beat
   celery -A OmniVisionAI beat -l info
   ```

### Automated Setup (Windows)
```powershell
# Run the automated setup script
.\start_server.ps1
```

## 🌐 Access Points

### Main Application
- **Dashboard**: http://127.0.0.1:8000/api/core/ui/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **API Documentation**: http://127.0.0.1:8000/api/docs/
- **Login**: http://127.0.0.1:8000/accounts/login/

### Default Credentials
- **Username**: `admin`
- **Password**: `admin123`

## 📊 Dashboard Features

### 🏠 **Overview Tab**
- Real-time system metrics
- Gate control panel with lock/unlock buttons
- Live camera feed grid (2x4 layout)
- System alerts and notifications
- Quick action buttons

### 👥 **Workers Tab**
- Worker registration with liveness detection
- Employee management and profiles
- Camera assignment for attendance
- Shift scheduling and department management

### 🚛 **Vehicles Tab**
- Vehicle registration and management
- Commercial vehicle support
- ANPR camera integration
- Authorization status tracking

### 🛡️ **PPE Detection Tab**
- Live PPE compliance monitoring
- Camera feeds for PPE detection
- Violation alerts and tracking

### 🧵 **Textile Monitoring Tab**
- Quality control monitoring
- Defect detection feeds
- Production status tracking

### ⚙️ **Settings Tab**
- System configuration
- User management
- Module settings

## 🔧 API Endpoints

### Core APIs
- `GET /api/core/dashboard/overview/` - Dashboard overview data
- `GET /api/core/cameras/` - Camera list
- `POST /api/core/cameras/` - Add new camera
- `GET /api/core/gates/` - Gate list
- `POST /api/core/gates/{id}/control/` - Control gate (lock/unlock)

### Worker APIs
- `GET /api/attendance/employees/` - Worker list
- `POST /api/attendance/employees/` - Register new worker

### Vehicle APIs
- `GET /api/vehicles/vehicles/` - Vehicle list
- `POST /api/vehicles/vehicles/` - Register new vehicle

## 🎨 UI/UX Features

### Design System
- **Color Palette**: Professional industrial colors
  - Primary: #0F172A (Dark Navy)
  - Secondary: #1E293B (Steel Gray)
  - Accent: #2563EB (Professional Blue)
  - Text: #F8FAFC (White)
  - Gray: #E2E8F0 (Light Gray)

### Interactive Elements
- **Smooth Transitions**: GSAP-powered animations
- **Hover Effects**: Subtle 3D effects and shadows
- **Responsive Design**: Mobile and tablet optimized
- **Tooltips**: Helpful hover information
- **Loading States**: Visual feedback for operations

### Navigation
- **Top Navigation**: Main module tabs
- **Side Panel**: Quick action buttons
- **Breadcrumbs**: Navigation context
- **Modal Forms**: Clean form interfaces

## 🔐 Security Features

- **JWT Authentication**: Secure API access
- **Session Management**: Secure login/logout
- **CSRF Protection**: Cross-site request forgery protection
- **Permission System**: Role-based access control
- **File Upload Security**: Secure file handling

## 📱 Responsive Design

### Desktop (1200px+)
- Full sidebar and navigation
- 2x4 camera grid layout
- Complete feature set

### Tablet (768px - 1199px)
- Collapsible sidebar
- Responsive grid layouts
- Touch-friendly controls

### Mobile (320px - 767px)
- Mobile-optimized navigation
- Single column layouts
- Touch gestures

## 🚀 Performance Features

### Real-time Updates
- **WebSocket Integration**: Live camera feeds
- **Auto-refresh**: Dashboard updates every 5 seconds
- **Live Metrics**: Real-time statistics
- **Instant Feedback**: Immediate UI updates

### Background Processing
- **Celery Tasks**: Background processing
- **Redis Caching**: Fast data access
- **Database Optimization**: Efficient queries
- **Static File Serving**: Optimized assets

## 🧪 Testing

### System Verification
```powershell
# Run system verification
.\test_system.ps1
```

### Manual Testing
1. **Login/Logout**: Test authentication flow
2. **Gate Control**: Test lock/unlock functionality
3. **Worker Registration**: Test liveness detection
4. **Vehicle Registration**: Test commercial vehicle support
5. **Camera Management**: Test camera addition and feeds

## 📈 Monitoring & Logs

### Health Checks
- API endpoint monitoring
- Database connection status
- Celery task monitoring
- WebSocket connection status

### Logging
- Django application logs
- Celery worker logs
- Access logs
- Error tracking

## 🔄 Maintenance

### Regular Tasks
- Database backups
- Log rotation
- Cache clearing
- System updates

### Troubleshooting
- Check Redis connection
- Verify Celery workers
- Monitor database performance
- Review error logs

## 📚 Documentation

### API Documentation
- Swagger UI: http://127.0.0.1:8000/api/docs/
- Interactive testing
- Request/response examples

### User Guides
- Dashboard navigation
- Worker registration process
- Vehicle management
- Gate control operations

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

### Code Standards
- Follow PEP 8 for Python
- Use meaningful variable names
- Add docstrings to functions
- Write unit tests

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Getting Help
- Check the documentation
- Review error logs
- Test system verification
- Contact support team

### Common Issues
- **Webcam not working**: Check browser permissions
- **Gate control failing**: Verify API endpoints
- **Camera feeds not loading**: Check WebSocket connection
- **Database errors**: Run migrations

---

## 🎉 **Ready to Use!**

The OmniVision AI system is now fully operational with all requested features implemented. The system provides comprehensive industrial monitoring capabilities with a professional, user-friendly interface.

**Next Steps:**
1. Access the dashboard at http://127.0.0.1:8000/api/core/ui/
2. Login with admin/admin123
3. Explore all modules and features
4. Register workers and vehicles
5. Configure cameras and gates
6. Monitor real-time data

**The system is ready for immediate use! 🚀**