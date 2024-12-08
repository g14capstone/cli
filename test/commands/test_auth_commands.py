import pytest
from unittest.mock import patch
from click.testing import CliRunner
from src.commands.key import (
    login,
    logout,
    create,
    list,
    delete_api_key,
    set_api_key,
    remove_api_key,
)


@pytest.fixture
def mock_auth_api():
    with patch("src.commands.auth_commands.AuthAPI") as mock:
        yield mock.return_value


@pytest.fixture
def runner():
    return CliRunner()


def test_login_command_success(runner, mock_auth_api):
    mock_auth_api.login.return_value = {"success": True, "data": "Login successful"}
    result = runner.invoke(
        login, ["--email", "test@example.com", "--password", "password"]
    )
    assert result.exit_code == 0
    assert "Successfully logged in" in result.output
    mock_auth_api.login.assert_called_once_with("test@example.com", "password")


def test_login_command_failure(runner, mock_auth_api):
    mock_auth_api.login.return_value = {
        "success": False,
        "message": "Invalid credentials",
    }
    result = runner.invoke(
        login, ["--email", "test@example.com", "--password", "wrong_password"]
    )
    assert result.exit_code == 0
    assert "Login failed. Invalid credentials" in result.output
    mock_auth_api.login.assert_called_once_with("test@example.com", "wrong_password")


def test_logout_command_success(runner, mock_auth_api):
    mock_auth_api.logout.return_value = True
    result = runner.invoke(logout)
    assert result.exit_code == 0
    assert "Successfully logged out" in result.output
    mock_auth_api.logout.assert_called_once()


def test_logout_command_not_logged_in(runner, mock_auth_api):
    mock_auth_api.logout.return_value = False
    result = runner.invoke(logout)
    assert result.exit_code == 0
    assert "No action taken. You were not logged in." in result.output
    mock_auth_api.logout.assert_called_once()


def test_create_api_key_command_success(runner, mock_auth_api):
    mock_auth_api.create_api_key.return_value = {"success": True, "data": "new_api_key"}
    result = runner.invoke(create, ["--validity", "ONE_DAY"])
    assert result.exit_code == 0
    assert "API key created successfully: new_api_key" in result.output
    mock_auth_api.create_api_key.assert_called_once()


def test_create_api_key_command_failure(runner, mock_auth_api):
    mock_auth_api.create_api_key.return_value = {
        "success": False,
        "message": "Failed to create API key",
    }
    result = runner.invoke(create, ["--validity", "ONE_DAY"])
    assert result.exit_code == 0
    assert "Failed to create API key. Failed to create API key" in result.output
    mock_auth_api.create_api_key.assert_called_once()


def test_list_api_keys_command_success(runner, mock_auth_api):
    mock_api_keys = [
        {"token": "key1", "created_at": "2023-01-01", "validity": "ONE_DAY"},
        {"token": "key2", "created_at": "2023-01-02", "validity": "ONE_WEEK"},
    ]
    mock_auth_api.list_api_keys.return_value = {"success": True, "data": mock_api_keys}
    result = runner.invoke(list)
    assert result.exit_code == 0
    assert "Token: key1" in result.output
    assert "Token: key2" in result.output
    mock_auth_api.list_api_keys.assert_called_once()


def test_list_api_keys_command_failure(runner, mock_auth_api):
    mock_auth_api.list_api_keys.return_value = {
        "success": False,
        "message": "Failed to retrieve API keys",
    }
    result = runner.invoke(list)
    assert result.exit_code == 0
    assert "Failed to retrieve API keys. Failed to retrieve API keys" in result.output
    mock_auth_api.list_api_keys.assert_called_once()


def test_delete_api_key_command_success(runner, mock_auth_api):
    mock_auth_api.delete_api_key.return_value = {
        "success": True,
        "data": "API key deleted",
    }
    result = runner.invoke(delete_api_key, ["--token", "test_token"])
    assert result.exit_code == 0
    assert "API key deleted successfully" in result.output
    mock_auth_api.delete_api_key.assert_called_once_with("test_token")


def test_delete_api_key_command_failure(runner, mock_auth_api):
    mock_auth_api.delete_api_key.return_value = {
        "success": False,
        "message": "API key not found",
    }
    result = runner.invoke(delete_api_key, ["--token", "invalid_token"])
    assert result.exit_code == 0
    assert "Failed to delete API key. API key not found" in result.output
    mock_auth_api.delete_api_key.assert_called_once_with("invalid_token")


def test_set_api_key_command_success(runner, mock_auth_api):
    mock_auth_api.set_api_key.return_value = True
    result = runner.invoke(set_api_key, ["--api-key", "new_api_key"])
    assert result.exit_code == 0
    assert "API key set successfully" in result.output
    mock_auth_api.set_api_key.assert_called_once_with("new_api_key")


def test_remove_api_key_command_success(runner, mock_auth_api):
    mock_auth_api.clear_api_key.return_value = True
    result = runner.invoke(remove_api_key)
    assert result.exit_code == 0
    assert "API key removed successfully" in result.output
    mock_auth_api.clear_api_key.assert_called_once()


def test_remove_api_key_command_no_key_set(runner, mock_auth_api):
    mock_auth_api.clear_api_key.return_value = False
    result = runner.invoke(remove_api_key)
    assert result.exit_code == 0
    assert "No API key was set" in result.output
    mock_auth_api.clear_api_key.assert_called_once()
