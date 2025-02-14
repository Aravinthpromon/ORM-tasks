import pytest
import base64
from rest_framework.test import APIClient
from django.contrib.auth.models import User

@pytest.fixture
def api_client():
    """Fixture to return API client with authentication"""
    client = APIClient()

    # Create a test user if it doesn't exist
    user, created = User.objects.get_or_create(username="admin")
    user.set_password("123")
    user.save()

    #  Log in the test user
    client.force_authenticate(user=user)

    #  Add authentication headers explicitly
    auth_credentials = "Basic " + base64.b64encode(b"admin:123").decode("utf-8")
    client.credentials(HTTP_AUTHORIZATION=auth_credentials)

    return client
