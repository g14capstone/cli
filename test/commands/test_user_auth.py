import unittest
from unittest.mock import patch
from click.testing import CliRunner
from src.commands.user_auth import login, logout


class TestUserAuth(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.runner = CliRunner()

        # Create and setup mock_auth_api
        self.patcher = patch("src.api.auth_api.AuthAPI")
        self.mock_auth_api = self.patcher.start()
        self.mock_instance = self.mock_auth_api.return_value

        self.endpoint = patch(
            "src.commands.user_auth.endpoint", self.mock_instance
        ).start()

    def tearDown(self):
        """Clean up after each test method."""
        self.patcher.stop()
        self.endpoint.stop()

    def test_login_success(self):
        """Test successful login."""
        self.mock_instance.login.return_value = {
            "success": True,
            "data": "Login successful",
        }

        with patch("click.echo") as mock_print:
            result = self.runner.invoke(
                login, ["--email", "test@test.com", "--password", "password"]
            )
            mock_print.assert_called_with("Successfully logged in. Login successful")
            self.assertEqual(result.exit_code, 0)

    def test_login_failure(self):
        """Test failed login."""
        self.mock_instance.login.return_value = {
            "success": False,
            "message": "Invalid credentials",
        }

        with patch("click.echo") as mock_print:
            result = self.runner.invoke(
                login, ["--email", "test@test.com", "--password", "wrong"]
            )
            mock_print.assert_called_with("Login failed. Invalid credentials")
            self.assertEqual(result.exit_code, 0)

    def test_logout_success(self):
        """Test successful logout."""
        self.mock_instance.logout.return_value = True

        with patch("click.echo") as mock_print:
            result = self.runner.invoke(logout)
            mock_print.assert_called_with("Successfully logged out.")
            self.assertEqual(result.exit_code, 0)

    def test_logout_not_logged_in(self):
        """Test logout when not logged in."""
        self.mock_instance.logout.return_value = False

        with patch("click.echo") as mock_print:
            result = self.runner.invoke(logout)
            mock_print.assert_called_with("No action taken. You were not logged in.")
            self.assertEqual(result.exit_code, 0)
