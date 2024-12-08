import unittest
from unittest.mock import patch
from click.testing import CliRunner

from src.api.machine_api import MachineAPI
from src.commands.machine import (
    list_machines,
    create_machine,
    start_machine,
    stop_machine,
    terminate_machine,
    get_machine_details,
)


class TestMachineCommands(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    @patch.object(MachineAPI, "list_user_machines")
    def test_list_user_machines_with_no_machines(self, mock_list_user_machines):
        mock_response = {"success": True, "data": []}
        mock_list_user_machines.return_value = mock_response

        result = self.runner.invoke(list_machines)

        self.assertEqual("No machines to list.\n", result.output)
        self.assertEqual(result.exit_code, 0)

    @patch.object(MachineAPI, "list_user_machines")
    def test_list_user_machines_with_some_machines(self, mock_list_user_machines):
        mock_list = [
            {
                "machine_id": "i-0dfa0b805940358fb",
                "machine_name": "test-cli-machine",
                "machine_type": "f1.2xlarge",
                "machine_status": "running",
                "hourly_price": 0.0116,
                "machine_desc": [
                    {"Key": "Name", "Value": "test-cli-machine-create"},
                    {"Key": "assigned", "Value": "true"},
                    {"Key": "user_id", "Value": "user_1234"},
                ],
            }
        ]
        mock_response = {"success": True, "data": mock_list}
        mock_list_user_machines.return_value = mock_response

        result = self.runner.invoke(list_machines)

        self.assertIn("Machines:\n" + str(mock_list[0]) + "\n", result.output)
        self.assertEqual(result.exit_code, 0)

    @patch.object(MachineAPI, "list_user_machines")
    def test_list_user_machines_fail(self, mock_list_user_machines):
        mock_response = {"success": False, "data": []}
        mock_list_user_machines.return_value = mock_response

        result = self.runner.invoke(list_machines)

        self.assertEqual("Failed to retrieve list of machines.\n", result.output)
        self.assertEqual(result.exit_code, 0)

    @patch.object(MachineAPI, "create_machine")
    def test_create_machine_success(self, mock_create_machine):
        mock_machine = {
            "machine_id": "i-0dfa0b805940358fb",
            "machine_name": "test-cli-machine",
            "machine_type": "f1.2xlarge",
            "machine_status": "running",
            "hourly_price": 0.0116,
            "machine_desc": [
                {"Key": "Name", "Value": "test-cli-machine-create"},
                {"Key": "assigned", "Value": "true"},
                {"Key": "user_id", "Value": "user_1234"},
            ],
        }
        mock_response = {"success": True, "data": mock_machine}
        mock_create_machine.return_value = mock_response

        result = self.runner.invoke(
            create_machine,
            ["--machine-name", "test-cli-machine", "--machine-type", "f1.2xlarge"],
        )

        self.assertIn(
            f"Machine created successfully. Details: {mock_machine}\n", result.output
        )
        self.assertEqual(result.exit_code, 0)

    @patch.object(MachineAPI, "create_machine")
    def test_create_machine_fail(self, mock_create_machine):
        mock_machine = {}
        mock_response = {"success": False, "data": mock_machine}
        mock_create_machine.return_value = mock_response

        result = self.runner.invoke(
            create_machine,
            ["--machine-name", "test-cli-machine", "--machine-type", "f1.2xlarge"],
        )

        self.assertIn(
            "Failed to create machine. Check machine name and type and try again.\n",
            result.output,
        )
        self.assertEqual(result.exit_code, 0)

    @patch.object(MachineAPI, "start_machine")
    def test_start_machine_success(self, mock_start_machine):
        mock_message = {"message": "Machine test1234 started successfully"}
        mock_response = {"success": True, "data": mock_message}
        mock_start_machine.return_value = mock_response

        result = self.runner.invoke(start_machine, ["--machine-id", "test1234"])

        self.assertIn("Machine test1234 started successfully\n", result.output)
        self.assertEqual(result.exit_code, 0)

    @patch.object(MachineAPI, "start_machine")
    def test_start_machine_fail(self, mock_start_machine):
        mock_message = {"message": "Failed"}
        mock_response = {"success": False, "data": mock_message}
        mock_start_machine.return_value = mock_response

        result = self.runner.invoke(start_machine, ["--machine-id", "test1234"])

        self.assertIn(
            "Failed to start machine. Check machine ID and try again.\n", result.output
        )
        self.assertEqual(result.exit_code, 0)

    @patch.object(MachineAPI, "stop_machine")
    def test_stop_machine_success(self, mock_stop_machine):
        mock_message = {"message": "Machine test1234 stopped successfully"}
        mock_response = {"success": True, "data": mock_message}
        mock_stop_machine.return_value = mock_response

        result = self.runner.invoke(stop_machine, ["--machine-id", "test1234"])

        self.assertIn("Machine test1234 stopped successfully\n", result.output)
        self.assertEqual(result.exit_code, 0)

    @patch.object(MachineAPI, "stop_machine")
    def test_stop_machine_fail(self, mock_stop_machine):
        mock_message = {"message": "Failed"}
        mock_response = {"success": False, "data": mock_message}
        mock_stop_machine.return_value = mock_response

        result = self.runner.invoke(stop_machine, ["--machine-id", "test1234"])

        self.assertIn(
            "Failed to stop machine. Check machine ID and try again.\n", result.output
        )
        self.assertEqual(result.exit_code, 0)

    @patch.object(MachineAPI, "terminate_machine")
    def test_terminate_machine_success(self, mock_terminate_machine):
        mock_message = {"message": "Machine test1234 terminated successfully"}
        mock_response = {"success": True, "data": mock_message}
        mock_terminate_machine.return_value = mock_response

        result = self.runner.invoke(terminate_machine, ["--machine-id", "test1234"])

        self.assertIn("Machine test1234 terminated successfully\n", result.output)
        self.assertEqual(result.exit_code, 0)

    @patch.object(MachineAPI, "terminate_machine")
    def test_terminate_machine_fail(self, mock_terminate_machine):
        mock_message = {"message": "Failed"}
        mock_response = {"success": False, "data": mock_message}
        mock_terminate_machine.return_value = mock_response

        result = self.runner.invoke(terminate_machine, ["--machine-id", "test1234"])

        self.assertIn(
            "Failed to terminate machine. Check machine ID and try again.\n",
            result.output,
        )
        self.assertEqual(result.exit_code, 0)

    @patch.object(MachineAPI, "get_machine")
    def test_get_machine_details_success(self, mock_get_machine):
        mock_machine = {
            "machine_id": "test1234",
            "machine_name": "test-cli-2",
            "machine_type": "f1.2xlarge",
            "machine_status": "running",
            "hourly_price": 0.0116,
            "machine_desc": [
                {"Key": "Name", "Value": "test-cli-2"},
                {"Key": "assigned", "Value": "true"},
                {"Key": "user_id", "Value": "user_1234"},
            ],
        }
        mock_response = {"success": True, "data": mock_machine}
        mock_get_machine.return_value = mock_response

        result = self.runner.invoke(get_machine_details, ["--machine-id", "test1234"])

        self.assertIn(
            "Machine test1234 details:\n" + str(mock_machine) + "\n", result.output
        )
        self.assertEqual(result.exit_code, 0)

    @patch.object(MachineAPI, "get_machine")
    def test_get_machine_details_fail(self, mock_get_machine):
        mock_machine = {"failed"}
        mock_response = {"success": False, "data": mock_machine}
        mock_get_machine.return_value = mock_response

        result = self.runner.invoke(get_machine_details, ["--machine-id", "test1234"])

        self.assertIn(
            "Failed to Get machine. Check machine ID and try again.\n", result.output
        )
        self.assertEqual(result.exit_code, 0)
