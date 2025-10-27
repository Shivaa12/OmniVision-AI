#!/usr/bin/env python
"""
Comprehensive test suite for OmniVision AI system
"""
import os
import sys
import django
import requests
import json
import time
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OmniVisionAI.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth.models import User
from core.models import Camera, Gate, Alert
from attendance.models import Employee
from vehicles.models import Vehicle

class OmniVisionAITests(TestCase):
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            is_staff=True,
            is_superuser=True
        )
        
        # Create test data
        self.camera = Camera.objects.create(
            name="Test Camera",
            ip_url="rtsp://test.com/stream",
            location="Test Location",
            camera_type="ip",
            purpose="attendance"
        )
        
        self.gate = Gate.objects.create(
            gate_number="TEST-001",
            location="Test Gate",
            status="locked"
        )
        
        self.employee = Employee.objects.create(
            name="Test Employee",
            employee_id="EMP001",
            role="operator"
        )
        
        self.vehicle = Vehicle.objects.create(
            registration_no="TEST123",
            vehicle_type="private",
            owner_name="Test Owner"
        )

    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/api/core/health/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('status', data)
        self.assertIn('database', data)
        self.assertIn('cache', data)

    def test_dashboard_overview(self):
        """Test dashboard overview endpoint"""
        response = self.client.get('/api/core/dashboard/overview/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('workers_present', data)
        self.assertIn('ppe_compliance', data)
        self.assertIn('vehicles', data)
        self.assertIn('gates', data)

    def test_camera_endpoints(self):
        """Test camera API endpoints"""
        # Test list
        response = self.client.get('/api/core/cameras/')
        self.assertEqual(response.status_code, 200)
        
        # Test create
        camera_data = {
            'name': 'New Test Camera',
            'ip_url': 'rtsp://newtest.com/stream',
            'location': 'New Location',
            'camera_type': 'ip',
            'purpose': 'ppe'
        }
        response = self.client.post('/api/core/cameras/', 
                                  data=json.dumps(camera_data),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_gate_endpoints(self):
        """Test gate API endpoints"""
        # Test list
        response = self.client.get('/api/core/gates/')
        self.assertEqual(response.status_code, 200)
        
        # Test gate control (requires authentication)
        self.client.force_login(self.user)
        control_data = {'action': 'unlock'}
        response = self.client.post(f'/api/core/gates/{self.gate.id}/control/',
                                  data=json.dumps(control_data),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_worker_endpoints(self):
        """Test worker API endpoints"""
        # Test list
        response = self.client.get('/api/attendance/employees/')
        self.assertEqual(response.status_code, 200)
        
        # Test create
        worker_data = {
            'name': 'New Test Worker',
            'employee_id': 'EMP002',
            'role': 'supervisor'
        }
        response = self.client.post('/api/attendance/employees/',
                                  data=json.dumps(worker_data),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_vehicle_endpoints(self):
        """Test vehicle API endpoints"""
        # Test list
        response = self.client.get('/api/vehicles/vehicles/')
        self.assertEqual(response.status_code, 200)
        
        # Test create
        vehicle_data = {
            'registration_no': 'NEW123',
            'vehicle_type': 'commercial',
            'owner_name': 'New Owner',
            'commercial_agency_name': 'Test Agency'
        }
        response = self.client.post('/api/vehicles/vehicles/',
                                  data=json.dumps(vehicle_data),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_authentication(self):
        """Test authentication endpoints"""
        # Test login page
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)
        
        # Test admin page
        self.client.force_login(self.user)
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

    def test_dashboard_ui(self):
        """Test dashboard UI endpoint"""
        response = self.client.get('/api/core/ui/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'OmniVision AI')

def run_integration_tests():
    """Run integration tests"""
    print("🧪 Running Integration Tests...")
    
    base_url = "http://127.0.0.1:8000"
    
    # Test health check
    try:
        response = requests.get(f"{base_url}/api/core/health/", timeout=5)
        if response.status_code == 200:
            print("✅ Health check: PASSED")
        else:
            print("❌ Health check: FAILED")
    except Exception as e:
        print(f"❌ Health check: ERROR - {e}")
    
    # Test dashboard overview
    try:
        response = requests.get(f"{base_url}/api/core/dashboard/overview/", timeout=5)
        if response.status_code == 200:
            print("✅ Dashboard overview: PASSED")
        else:
            print("❌ Dashboard overview: FAILED")
    except Exception as e:
        print(f"❌ Dashboard overview: ERROR - {e}")
    
    # Test camera endpoints
    try:
        response = requests.get(f"{base_url}/api/core/cameras/", timeout=5)
        if response.status_code == 200:
            print("✅ Camera endpoints: PASSED")
        else:
            print("❌ Camera endpoints: FAILED")
    except Exception as e:
        print(f"❌ Camera endpoints: ERROR - {e}")
    
    # Test gate endpoints
    try:
        response = requests.get(f"{base_url}/api/core/gates/", timeout=5)
        if response.status_code == 200:
            print("✅ Gate endpoints: PASSED")
        else:
            print("❌ Gate endpoints: FAILED")
    except Exception as e:
        print(f"❌ Gate endpoints: ERROR - {e}")
    
    # Test worker endpoints
    try:
        response = requests.get(f"{base_url}/api/attendance/employees/", timeout=5)
        if response.status_code == 200:
            print("✅ Worker endpoints: PASSED")
        else:
            print("❌ Worker endpoints: FAILED")
    except Exception as e:
        print(f"❌ Worker endpoints: ERROR - {e}")
    
    # Test vehicle endpoints
    try:
        response = requests.get(f"{base_url}/api/vehicles/vehicles/", timeout=5)
        if response.status_code == 200:
            print("✅ Vehicle endpoints: PASSED")
        else:
            print("❌ Vehicle endpoints: FAILED")
    except Exception as e:
        print(f"❌ Vehicle endpoints: ERROR - {e}")
    
    # Test admin interface
    try:
        response = requests.get(f"{base_url}/admin/", timeout=5)
        if response.status_code in [200, 302]:  # 302 for redirect to login
            print("✅ Admin interface: PASSED")
        else:
            print("❌ Admin interface: FAILED")
    except Exception as e:
        print(f"❌ Admin interface: ERROR - {e}")
    
    # Test API documentation
    try:
        response = requests.get(f"{base_url}/api/docs/", timeout=5)
        if response.status_code == 200:
            print("✅ API documentation: PASSED")
        else:
            print("❌ API documentation: FAILED")
    except Exception as e:
        print(f"❌ API documentation: ERROR - {e}")

if __name__ == "__main__":
    print("🚀 OmniVision AI - Comprehensive Test Suite")
    print("=" * 50)
    
    # Run Django tests
    print("\n📋 Running Django Unit Tests...")
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'test', '--verbosity=2'])
    
    # Run integration tests
    print("\n🔗 Running Integration Tests...")
    run_integration_tests()
    
    print("\n✅ Test suite completed!")
    print("=" * 50)
