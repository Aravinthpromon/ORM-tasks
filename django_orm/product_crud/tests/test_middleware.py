import pytest
import base64
from django.urls import reverse
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    """Fixture to set up API client"""
    return APIClient()

@pytest.mark.django_db
def test_basic_auth_middleware_unauthorized(api_client):
    """Test if the middleware blocks requests without authentication"""
    response = api_client.get(reverse('category_handler'))  # Access API without credentials
    assert response.status_code == 401
    assert "error" in response.json()
    assert response.json()["error"] == "Missing or invalid Authorization header"

@pytest.mark.django_db
def test_basic_auth_middleware_authorized(api_client):
    """Test if the middleware allows access when correct credentials are provided"""
    credentials = "Basic " + base64.b64encode(b"admin:123").decode("utf-8")  # Encoding "admin:123"
    api_client.credentials(HTTP_AUTHORIZATION=credentials)

    response = api_client.get(reverse('category_handler'))  # Access API with credentials
    assert response.status_code != 401  # Ensure it's NOT unauthorized
