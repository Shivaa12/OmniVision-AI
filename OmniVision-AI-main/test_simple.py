#!/usr/bin/env python
"""
Simple test suite for OmniVision AI system
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

def run_integration_tests():
    """Run integration tests"""
    print("Running Integration Tests...")
    
    base_url = "http://127.0.0.1:8000"
    
    # Test health check
    try:
        response = requests.get(f"{base_url}/api/core/health/", timeout=5)
        if response.status_code == 200:
            print("Health check: PASSED")
        else:
            print("Health check: FAILED")
    except Exception as e:
        print(f"Health check: ERROR - {e}")
    
    # Test dashboard overview
    try:
        response = requests.get(f"{base_url}/api/core/dashboard/overview/", timeout=5)
        if response.status_code == 200:
            print("Dashboard overview: PASSED")
        else:
            print("Dashboard overview: FAILED")
    except Exception as e:
        print(f"Dashboard overview: ERROR - {e}")
    
    # Test camera endpoints
    try:
        response = requests.get(f"{base_url}/api/core/cameras/", timeout=5)
        if response.status_code == 200:
            print("Camera endpoints: PASSED")
        else:
            print("Camera endpoints: FAILED")
    except Exception as e:
        print(f"Camera endpoints: ERROR - {e}")
    
    # Test gate endpoints
    try:
        response = requests.get(f"{base_url}/api/core/gates/", timeout=5)
        if response.status_code == 200:
            print("Gate endpoints: PASSED")
        else:
            print("Gate endpoints: FAILED")
    except Exception as e:
        print(f"Gate endpoints: ERROR - {e}")
    
    # Test worker endpoints
    try:
        response = requests.get(f"{base_url}/api/attendance/employees/", timeout=5)
        if response.status_code == 200:
            print("Worker endpoints: PASSED")
        else:
            print("Worker endpoints: FAILED")
    except Exception as e:
        print(f"Worker endpoints: ERROR - {e}")
    
    # Test vehicle endpoints
    try:
        response = requests.get(f"{base_url}/api/vehicles/vehicles/", timeout=5)
        if response.status_code == 200:
            print("Vehicle endpoints: PASSED")
        else:
            print("Vehicle endpoints: FAILED")
    except Exception as e:
        print(f"Vehicle endpoints: ERROR - {e}")
    
    # Test admin interface
    try:
        response = requests.get(f"{base_url}/admin/", timeout=5)
        if response.status_code in [200, 302]:  # 302 for redirect to login
            print("Admin interface: PASSED")
        else:
            print("Admin interface: FAILED")
    except Exception as e:
        print(f"Admin interface: ERROR - {e}")
    
    # Test API documentation
    try:
        response = requests.get(f"{base_url}/api/docs/", timeout=5)
        if response.status_code == 200:
            print("API documentation: PASSED")
        else:
            print("API documentation: FAILED")
    except Exception as e:
        print(f"API documentation: ERROR - {e}")

if __name__ == "__main__":
    print("OmniVision AI - Test Suite")
    print("=" * 50)
    
    # Run integration tests
    print("\nRunning Integration Tests...")
    run_integration_tests()
    
    print("\nTest suite completed!")
    print("=" * 50)
