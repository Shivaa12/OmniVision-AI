from django.urls import reverse
from rest_framework.test import APIClient
import pytest


@pytest.mark.django_db
def test_dashboard_overview_requires_auth():
    client = APIClient()
    url = "/api/core/dashboard/overview/"
    resp = client.get(url)
    assert resp.status_code in (401, 403)


@pytest.mark.django_db
def test_dashboard_overview_authenticated(admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    url = "/api/core/dashboard/overview/"
    resp = client.get(url)
    assert resp.status_code == 200
    data = resp.json()
    assert "workers_present" in data
    assert "ppe_compliance" in data
    assert "vehicles" in data
    assert "textile_defects" in data

