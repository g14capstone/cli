import unittest
from unittest.mock import MagicMock, patch
from click.testing import CliRunner
from src.commands.model_file import model, ModelFileCommands
import traceback


class TestModelFileCommands(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.runner = CliRunner()

        # Create and setup mock_model_api
        self.patcher = patch("src.api.model_file_api.ModelFileAPI")
        self.mock_model_api = self.patcher.start()
        self.mock_instance = self.mock_model_api.return_value

        # Set up default successful responses
        self.mock_instance.upload_model_file.return_value = {
            "success": True,
            "data": {
                "model_name": "test_model",
                "model_id": "123",
                "upload_date": "2023-01-01T12:00:00.000+0000",
            },
        }
        self.mock_instance.get_all_models.return_value = {
            "success": True,
            "data": [],
            "response": {"detail": None},
        }
        self.mock_instance.get_model.return_value = {
            "success": True,
            "data": {"model_name": "test_model", "model_id": "123", "files": []},
        }
        self.mock_instance.read_model_file.return_value = {
            "success": True,
            "data": {"content": "test content"},
        }
        self.mock_instance.delete_model_file.return_value = {
            "success": True,
            "data": None,
        }
        self.mock_instance.delete_model.return_value = {"success": True, "data": None}

        # Setup model_commands
        self.model_commands = ModelFileCommands()
        self.model_commands.client = MagicMock()
        self.model_commands.endpoint = self.mock_instance

    def tearDown(self):
        """Clean up after each test method."""
        self.patcher.stop()

    def test_upload_model_file_success(self):
        with patch("click.echo") as mock_print:
            self.model_commands.upload("test.txt", "test_model")
            mock_print.assert_any_call("\nAttempting to upload model file...\n")
            mock_print.assert_any_call("Model file uploaded successfully:")

    def test_upload_model_file_failure(self):
        self.mock_instance.upload_model_file.return_value = {
            "success": False,
            "response": {"detail": "Upload failed"},
        }
        with patch("click.echo") as mock_print:
            self.model_commands.upload("test.txt", "test_model")
            mock_print.assert_called_with("Failed to upload model file: Upload failed")

    def test_list_models_success(self):
        mock_models = [
            {
                "model_name": "model1",
                "model_id": "123",
                "files": [
                    {
                        "file_name": "test.txt",
                        "file_size": 100,
                        "last_modified": "2023-01-01T12:00:00Z",
                    }
                ],
            }
        ]
        self.mock_instance.get_all_models.return_value = {
            "success": True,
            "data": mock_models,
        }
        with patch("click.echo") as mock_print:
            self.model_commands.list()
            mock_print.assert_any_call("Default Models:")

    def test_get_model_success(self):
        with patch("click.echo") as mock_print:
            self.model_commands.get_model("123")
            mock_print.assert_any_call("Name: test_model")
            mock_print.assert_any_call("ID: 123")

    def test_read_file_success(self):
        with patch("click.echo") as mock_print:
            self.model_commands.read_file("123", "test.txt")
            mock_print.assert_any_call("File contents for test.txt:")
            mock_print.assert_any_call("test content")

    def test_delete_file_success(self):
        with patch("click.echo") as mock_print:
            self.model_commands.delete_file("123", "test.txt")
            mock_print.assert_called_with("Model file test.txt deleted successfully")

    def test_delete_model_success(self):
        with patch("click.echo") as mock_print:
            self.model_commands.delete_model("123")
            mock_print.assert_called_with("Model 123 deleted successfully")

    @patch("src.commands.model_file.ModelFileCommands", autospec=True)
    def test_cli_upload_command(self, model_commands):
        with self.runner.isolated_filesystem():
            with open("test.txt", "w") as f:
                f.write("test")
            result = self.runner.invoke(
                model, ["upload", "-n", "test_model", "-f", "test.txt"]
            )
            self.assertEqual(result.exit_code, 0)

    @patch("src.commands.model_file.ModelFileCommands", autospec=True)
    def test_cli_list_command(self, model_commands):
        result = self.runner.invoke(model, ["list"])
        if result.exit_code != 0:
            print(f"Exit code: {result.exit_code}")
            print(f"Output: {result.output}")
            print(f"Exception: {result.exception}")
            if result.exc_info:
                print("Full traceback:")
                print("".join(traceback.format_exception(*result.exc_info)))
        self.assertEqual(result.exit_code, 0)

    @patch("src.commands.model_file.ModelFileCommands", autospec=True)
    def test_cli_get_command(self, model_commands):
        result = self.runner.invoke(model, ["get", "--model-id", "123"])
        print(result.output)
        self.assertEqual(result.exit_code, 0)

    @patch("src.commands.model_file.ModelFileCommands", autospec=True)
    def test_cli_delete_command(self, model_commands):
        result = self.runner.invoke(model, ["delete", "--model-id", "123"])
        self.assertEqual(result.exit_code, 0)
