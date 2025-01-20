import unittest
from unittest.mock import patch
from click.testing import CliRunner
from src.commands.user_auth import login, logout, register


class TestUserAuth(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.runner = CliRunner()

        # Create and setup mock_auth_api
        self.auth_patcher = patch("src.api.auth_api.AuthAPI")
        self.mock_auth_api = self.auth_patcher.start()
        self.mock_instance = self.mock_auth_api.return_value

        self.endpoint = patch(
            "src.commands.user_auth.endpoint", self.mock_instance
        ).start()

        # Create and setup mock_user_api
        self.user_patcher = patch("src.api.user_api.UserAPI")
        self.mock_user_api = self.user_patcher.start()
        self.mock_user_instance = self.mock_user_api.return_value

        self.user_endpoint = patch(
            "src.commands.user_auth.user_endpoint", self.mock_user_instance
        ).start()

    def tearDown(self):
        """Clean up after each test method."""
        self.auth_patcher.stop()
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

    def test_logout_failure(self):
        """Test logout failure."""
        self.mock_instance.logout.return_value = False

        with patch("click.echo") as mock_print:
            result = self.runner.invoke(logout)
            mock_print.assert_called_with("No action taken. You were not logged in.")
            self.assertEqual(result.exit_code, 0)

    def test_register_success(self):
        """Test successful registration."""
        self.mock_user_instance.register.return_value = {
            "success": True,
            "data": {
                "user_name": "test_user",
                "email": "test@user.ca",
                "user_id": "123",
            },
        }
        self.mock_instance.login.return_value = {
            "success": True,
            "data": "Login successful",
        }

        with patch("click.echo") as mock_print:
            result = self.runner.invoke(
                register,
                [
                    "--username",
                    "test_user",
                    "--email",
                    "test@user.ca",
                    "--password",
                    "password",
                ],
            )
            mock_print.assert_any_call(
                "Welcome to Duckington Labs, you've successfully registered as:"
            )
            mock_print.assert_any_call("  - Username: test_user")
            mock_print.assert_any_call("  - Email: test@user.ca")
            mock_print.assert_any_call("  - User ID: 123")
            mock_print.assert_any_call("Successfully logged in. Login successful")
            self.assertEqual(result.exit_code, 0)

    def test_register_failure(self):
        """Test failed registration."""
        self.mock_user_instance.register.return_value = {
            "success": False,
            "message": "Registration failed",
        }

        with patch("click.echo") as mock_print:
            result = self.runner.invoke(
                register,
                [
                    "--username",
                    "test_user",
                    "--email",
                    "test@user.ca",
                    "--password",
                    "password",
                ],
            )
            mock_print.assert_called_with("Login failed. Registration failed")
            self.assertEqual(result.exit_code, 0)
