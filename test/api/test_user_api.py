import pytest
from unittest.mock import Mock
from src.api.user_api import UserAPI


@pytest.fixture
def mock_client():
    return Mock()


@pytest.fixture
def user_api(mock_client):
    return UserAPI(mock_client)


def test_register_success(user_api, mock_client):
    mock_client.post.return_value = {
        "user_id": "12345",
        "user_name": "testuser",
        "email": "test@test.com",
    }

    result = user_api.register("testuser", "test@test.com", "password")

    assert result["data"]["user_id"] == "12345"
    assert result["data"]["user_name"] == "testuser"
    assert result["data"]["email"] == "test@test.com"
    mock_client.post.assert_called_once_with(
        "user",
        data={
            "user_name": "testuser",
            "email": "test@test.com",
            "password": "password",
        },
    )


def test_register_failure(user_api, mock_client):
    mock_client.post.return_value = {"error": "Registration failed"}

    result = user_api.register("testuser", "test@test.com", "password")

    assert result == {
        "success": False,
        "error": "Unexpected error",
        "message": "Failed to register: {'error': 'Registration failed'}",
    }

    mock_client.post.assert_called_once_with(
        "user",
        data={
            "user_name": "testuser",
            "email": "test@test.com",
            "password": "password",
        },
    )
