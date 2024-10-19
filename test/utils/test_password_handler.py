import pytest
from unittest.mock import patch
from src.utils.password_handler import PasswordHandler
import keyring


@pytest.fixture
def password_handler():
    return PasswordHandler("test_service")


def test_set_password(password_handler):
    with patch("keyring.set_password") as mock_set:
        password_handler.set_password("test_key", "test_value")
        mock_set.assert_called_once_with("test_service", "test_key", "test_value")


def test_get_password(password_handler):
    with patch("keyring.get_password", return_value="test_value") as mock_get:
        result = password_handler.get_password("test_key")
        assert result == "test_value"
        mock_get.assert_called_once_with("test_service", "test_key")


def test_delete_password_success(password_handler):
    with patch("keyring.delete_password") as mock_delete:
        result = password_handler.delete_password("test_key")
        assert result is True
        mock_delete.assert_called_once_with("test_service", "test_key")


def test_delete_password_failure(password_handler):
    with patch(
        "keyring.delete_password", side_effect=keyring.errors.PasswordDeleteError
    ):
        result = password_handler.delete_password("test_key")
        assert result is False
