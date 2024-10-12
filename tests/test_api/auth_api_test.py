import pytest
from unittest.mock import Mock, patch
from src.api.auth_api import AuthAPI
from src.utils.helpers.validity_enum import ValidityEnum


@pytest.fixture
def mock_client():
    return Mock()


@pytest.fixture
def auth_api(mock_client):
    return AuthAPI(mock_client)


def test_login_success(auth_api, mock_client):
    mock_client.post.return_value = {"access_token": "test_token"}
    result = auth_api.login("test_user", "test_password")
    assert result == {"success": True, "data": "Login successful"}
    mock_client.set_access_token.assert_called_once_with("test_token")


def test_login_failure(auth_api, mock_client):
    mock_client.post.return_value = {"error": "Invalid credentials"}
    result = auth_api.login("test_user", "wrong_password")
    assert result == {
        "success": False,
        "error": "Unexpected error",
        "message": "Failed to login: {'error': 'Invalid credentials'}",
    }


def test_logout(auth_api, mock_client):
    auth_api.logout()
    mock_client.clear_access_token.assert_called_once()


def test_set_api_key(auth_api, mock_client):
    auth_api.set_api_key("test_api_key")
    mock_client.set_api_key.assert_called_once_with("test_api_key")


def test_clear_api_key(auth_api, mock_client):
    auth_api.clear_api_key()
    mock_client.clear_api_key.assert_called_once()


def test_create_api_key(auth_api, mock_client):
    mock_client.get.return_value = "new_api_key"
    result = auth_api.create_api_key(ValidityEnum.ONE_DAY)
    assert result == {"success": True, "data": "new_api_key"}
    mock_client.get.assert_called_once_with("auth/api_key/one_day")


def test_list_api_keys(auth_api, mock_client):
    mock_response = [
        {"token": "key1", "created_at": "2023-01-01", "validity": "ONE_DAY"}
    ]
    mock_client.get.return_value = mock_response
    result = auth_api.list_api_keys()
    assert result == {"success": True, "data": mock_response}
    mock_client.get.assert_called_once_with("auth/api_keys")


def test_delete_api_key(auth_api, mock_client):
    mock_client.delete.return_value = "API key deleted"
    result = auth_api.delete_api_key("test_token")
    assert result == {"success": True, "data": "API key deleted"}
    mock_client.delete.assert_called_once_with("auth/api_key/test_token")
