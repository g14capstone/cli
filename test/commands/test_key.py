import unittest
from unittest.mock import MagicMock, patch
from click.testing import CliRunner
from src.commands.key import key, KeyCommands


class TestKeyCommands(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.runner = CliRunner()

        # Create and setup mock_auth_api
        self.patcher = patch("src.api.auth_api.AuthAPI")
        self.mock_auth_api = self.patcher.start()
        self.mock_instance = self.mock_auth_api.return_value

        # Set up default successful responses
        self.mock_instance.create_api_key.return_value = {
            "success": True,
            "data": "test_key",
        }
        self.mock_instance.list_api_keys.return_value = {"success": True, "data": []}
        self.mock_instance.delete_api_key.return_value = {
            "success": True,
            "data": "Deleted",
        }
        self.mock_instance.set_api_key.return_value = True
        self.mock_instance.clear_api_key.return_value = True

        # Setup key_commands
        self.key_commands = KeyCommands()
        self.key_commands.client = MagicMock()
        self.key_commands.endpoint = self.mock_instance

    def tearDown(self):
        """Clean up after each test method."""
        self.patcher.stop()

    def test_create_api_key_success(self):
        self.mock_instance.create_api_key.return_value = {
            "success": True,
            "data": "new_api_key",
        }

        with patch("click.echo") as mock_print:
            self.key_commands.create_api_key("ONE_DAY")
            mock_print.assert_called_with("API key created successfully: new_api_key")

    def test_create_api_key_failure(self):
        self.mock_instance.create_api_key.return_value = {
            "success": False,
            "message": "Failed to create key",
        }

        with patch("click.echo") as mock_print:
            self.key_commands.create_api_key("ONE_DAY")
            mock_print.assert_called_with(
                "Failed to create API key. Failed to create key"
            )

    def test_list_api_keys_success(self):
        mock_keys = [
            {"token": "key1", "created_at": "2023-01-01", "validity": "ONE_DAY"},
            {"token": "key2", "created_at": "2023-01-02", "validity": "ONE_WEEK"},
        ]
        self.mock_instance.list_api_keys.return_value = {
            "success": True,
            "data": mock_keys,
        }

        with patch("click.echo") as mock_print:
            self.key_commands.list_api_keys()
            self.assertEqual(mock_print.call_count, 3)

    def test_list_api_keys_empty(self):
        self.mock_instance.list_api_keys.return_value = {"success": True, "data": []}

        with patch("click.echo") as mock_print:
            self.key_commands.list_api_keys()
            mock_print.assert_called_with("API Keys:")

    def test_delete_api_key_success(self):
        self.mock_instance.delete_api_key.return_value = {
            "success": True,
            "data": "Key deleted",
        }

        with patch("click.echo") as mock_print:
            self.key_commands.delete_api_key("test_token")
            mock_print.assert_called_with("API key deleted successfully. Key deleted")

    def test_delete_api_key_failure(self):
        self.mock_instance.delete_api_key.return_value = {
            "success": False,
            "message": "Key not found",
        }

        with patch("click.echo") as mock_print:
            self.key_commands.delete_api_key("invalid_token")
            mock_print.assert_called_with("Failed to delete API key. Key not found")

    def test_set_api_key_success(self):
        self.mock_instance.set_api_key.return_value = True

        with patch("click.echo") as mock_print:
            self.key_commands.set_api_key("test_key")
            mock_print.assert_called_with("API key set successfully.")

    def test_remove_api_key_success(self):
        self.mock_instance.clear_api_key.return_value = True

        with patch("click.echo") as mock_print:
            self.key_commands.remove_api_key()
            mock_print.assert_called_with("API key removed successfully.")

    def test_remove_api_key_no_key(self):
        self.mock_instance.clear_api_key.return_value = False

        with patch("click.echo") as mock_print:
            self.key_commands.remove_api_key()
            mock_print.assert_called_with("No API key was set.")

    @patch("src.commands.key.KeyCommands", autospec=True)
    def test_cli_create_command(self, key_commands):
        result = self.runner.invoke(key, ["create", "--validity", "ONE_DAY"])
        self.assertEqual(result.exit_code, 0)

    @patch("src.commands.key.KeyCommands", autospec=True)
    def test_cli_list_command(self, key_commands):
        result = self.runner.invoke(key, ["list"])
        self.assertEqual(result.exit_code, 0)

    @patch("src.commands.key.KeyCommands", autospec=True)
    def test_cli_delete_command(self, key_commands):
        result = self.runner.invoke(key, ["delete", "--token", "test_token"])
        self.assertEqual(result.exit_code, 0)

    @patch("src.commands.key.KeyCommands", autospec=True)
    def test_cli_set_command(self, key_commands):
        result = self.runner.invoke(key, ["set", "--api-key", "test_key"])
        self.assertEqual(result.exit_code, 0)

    @patch("src.commands.key.KeyCommands", autospec=True)
    def test_cli_unset_command(self, key_commands):
        result = self.runner.invoke(key, ["unset"])
        self.assertEqual(result.exit_code, 0)
