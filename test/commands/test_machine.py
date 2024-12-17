import unittest
from unittest.mock import MagicMock, patch
from click.testing import CliRunner
from src.commands.machine import MachineCommands, machine


class TestMachineCommands(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.runner = CliRunner()

        # Create and setup mock_machine_api
        self.patcher = patch("src.api.machine_api.MachineAPI")
        self.mock_machine_api = self.patcher.start()
        self.mock_instance = self.mock_machine_api.return_value

        # Set up default successful responses
        self.mock_instance.create_machine.return_value = {
            "success": True,
            "data": {
                "machine_id": "test123",
                "machine_name": "test-machine",
                "machine_type": "f1.2xlarge",
            },
        }
        self.mock_instance.list_user_machines.return_value = {
            "success": True,
            "data": [],
        }
        self.mock_instance.start_machine.return_value = {
            "success": True,
            "data": {"message": "Machine started successfully"},
        }
        self.mock_instance.stop_machine.return_value = {
            "success": True,
            "data": {"message": "Machine stopped successfully"},
        }
        self.mock_instance.terminate_machine.return_value = {
            "success": True,
            "data": {"message": "Machine terminated successfully"},
        }

        # Setup machine_commands
        self.machine_commands = MachineCommands()
        self.machine_commands.client = MagicMock()
        self.machine_commands.endpoint = self.mock_instance

    def tearDown(self):
        """Clean up after each test method."""
        self.patcher.stop()

    def test_create_machine_success(self):
        with patch("click.echo") as mock_print:
            self.machine_commands.create("test-machine", "f1.2xlarge")
            mock_print.assert_called_with(
                f"Machine created successfully. Details: {self.mock_instance.create_machine.return_value['data']}"
            )

    def test_create_machine_failure(self):
        self.mock_instance.create_machine.return_value = {
            "success": False,
            "message": "Failed to create machine",
        }

        with patch("click.echo") as mock_print:
            self.machine_commands.create("test-machine", "f1.2xlarge")
            mock_print.assert_called_with(
                "Failed to create machine. Check machine name and type and try again."
            )

    def test_list_machines_with_data(self):
        mock_machines = [
            {"machine_id": "test123", "machine_name": "test-machine-1"},
            {"machine_id": "test456", "machine_name": "test-machine-2"},
        ]
        self.mock_instance.list_user_machines.return_value = {
            "success": True,
            "data": mock_machines,
        }

        with patch("click.echo") as mock_print:
            self.machine_commands.list()
            self.assertEqual(mock_print.call_count, 3)  # Header + 2 machines

    def test_list_machines_empty(self):
        with patch("click.echo") as mock_print:
            self.machine_commands.list()
            mock_print.assert_called_with("No machines to list.")

    def test_start_machine_success(self):
        with patch("click.echo") as mock_print:
            self.machine_commands.start("test123")
            mock_print.assert_called_with("Machine started successfully")

    def test_stop_machine_success(self):
        with patch("click.echo") as mock_print:
            self.machine_commands.stop("test123")
            mock_print.assert_called_with("Machine stopped successfully")

    def test_terminate_machine_success(self):
        with patch("click.echo") as mock_print:
            self.machine_commands.terminate("test123")
            mock_print.assert_called_with("Machine terminated successfully")

    def test_get_machine_details_success(self):
        self.mock_instance.get_machine.return_value = {
            "success": True,
            "data": {
                "machine_id": "test123",
                "machine_name": "test-machine",
                "machine_type": "f1.2xlarge",
            },
        }

        with patch("click.echo") as mock_print:
            self.machine_commands.get_details("test123")
            self.assertEqual(mock_print.call_count, 2)

    # CLI command tests
    def test_cli_create_command(self):
        result = self.runner.invoke(
            machine,
            ["create", "-n", "test-machine", "-t", "f1.2xlarge"],
        )
        self.assertEqual(result.exit_code, 0)

    def test_cli_list_command(self):
        result = self.runner.invoke(machine, ["list"])
        self.assertEqual(result.exit_code, 0)

    def test_cli_start_command(self):
        result = self.runner.invoke(machine, ["start", "--machine-id", "test123"])
        self.assertEqual(result.exit_code, 0)

    def test_cli_stop_command(self):
        result = self.runner.invoke(machine, ["stop", "--machine-id", "test123"])
        self.assertEqual(result.exit_code, 0)

    def test_cli_terminate_command(self):
        result = self.runner.invoke(machine, ["terminate", "--machine-id", "test123"])
        self.assertEqual(result.exit_code, 0)

    def test_cli_details_command(self):
        result = self.runner.invoke(machine, ["details", "--machine-id", "test123"])
        self.assertEqual(result.exit_code, 0)


if __name__ == "__main__":
    unittest.main()
