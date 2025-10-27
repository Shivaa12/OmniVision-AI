Write-Host "========================================" -ForegroundColor Cyan
Write-Host "OmniVision AI - System Verification" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Test API endpoints
Write-Host "Testing API Endpoints..." -ForegroundColor Yellow

try {
    $overview = Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/core/dashboard/overview/" -UseBasicParsing
    if ($overview.StatusCode -eq 200) {
        Write-Host "✅ Overview API: Working" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Overview API: Failed" -ForegroundColor Red
}

try {
    $workers = Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/attendance/employees/" -UseBasicParsing
    if ($workers.StatusCode -eq 200) {
        Write-Host "✅ Workers API: Working" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Workers API: Failed" -ForegroundColor Red
}

try {
    $vehicles = Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/vehicles/vehicles/" -UseBasicParsing
    if ($vehicles.StatusCode -eq 200) {
        Write-Host "✅ Vehicles API: Working" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Vehicles API: Failed" -ForegroundColor Red
}

try {
    $cameras = Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/core/cameras/" -UseBasicParsing
    if ($cameras.StatusCode -eq 200) {
        Write-Host "✅ Cameras API: Working" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Cameras API: Failed" -ForegroundColor Red
}

try {
    $admin = Invoke-WebRequest -Uri "http://127.0.0.1:8000/admin/" -UseBasicParsing
    if ($admin.StatusCode -eq 200) {
        Write-Host "✅ Admin Interface: Working" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Admin Interface: Failed" -ForegroundColor Red
}

try {
    $docs = Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/docs/" -UseBasicParsing
    if ($docs.StatusCode -eq 200) {
        Write-Host "✅ API Documentation: Working" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ API Documentation: Failed" -ForegroundColor Red
}

try {
    $login = Invoke-WebRequest -Uri "http://127.0.0.1:8000/accounts/login/" -UseBasicParsing
    if ($login.StatusCode -eq 200) {
        Write-Host "✅ Login Page: Working" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Login Page: Failed" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "System Verification Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🚀 Ready to use OmniVision AI!" -ForegroundColor Yellow
Write-Host ""
Write-Host "Access the system at:" -ForegroundColor White
Write-Host "Main Dashboard: http://127.0.0.1:8000/api/core/ui/" -ForegroundColor Cyan
Write-Host "Admin: http://127.0.0.1:8000/admin/" -ForegroundColor Cyan
Write-Host "API Docs: http://127.0.0.1:8000/api/docs/" -ForegroundColor Cyan
Write-Host ""
Write-Host "Credentials: admin / admin123" -ForegroundColor Yellow
