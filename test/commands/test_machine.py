import json
import unittest
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from src.commands.machine import MachineCommands, machine


class TestNewMachineCommands(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.runner = CliRunner()

        # Create and setup mock_machine_api
        self.patcher = patch("src.api.machine_api.MachineAPI")
        self.mock_machine_api = self.patcher.start()
        self.mock_instance = self.mock_machine_api.return_value

        # Set up default successful responses
        self.mock_instance.create_gpu_machine.return_value = {
            "success": True,
            "data": {
                "machine_id": "test123",
                "machine_name": "test-machine",
                "machine_type": "g4dn.xlarge",
            },
        }
        self.mock_instance.create_fpga_machine.return_value = {
            "success": True,
            "data": {
                "machine_id": "test123",
                "machine_name": "test-machine",
                "machine_type": "f1.2xlarge",
            },
        }
        self.mock_instance.create_cpu_machine.return_value = {
            "success": True,
            "data": {
                "machine_id": "test123",
                "machine_name": "test-machine",
                "machine_type": "t2.micro",
            },
        }
        self.mock_instance.pull_gpu_model.return_value = {
            "success": True,
            "data": {"message": "Model pulled successfully"},
        }
        self.mock_instance.pull_cpu_model.return_value = {
            "success": True,
            "data": {"message": "Model pulled successfully"},
        }
        self.mock_instance.delete_gpu_model.return_value = {
            "success": True,
            "data": {"message": "Model deleted successfully"},
        }
        self.mock_instance.delete_cpu_model.return_value = {
            "success": True,
            "data": {"message": "Model deleted successfully"},
        }
        self.mock_instance.get_gpu_inference_url.return_value = {
            "success": True,
            "data": {"inference_url": "http://gpu-inference-url"},
        }
        self.mock_instance.get_cpu_inference_url.return_value = {
            "success": True,
            "data": {"inference_url": "http://cpu-inference-url"},
        }

        # Setup machine_commands
        self.machine_commands = MachineCommands()
        self.machine_commands.client = MagicMock()
        self.machine_commands.endpoint = self.mock_instance

    def tearDown(self):
        """Clean up after each test method."""
        self.patcher.stop()

    def test_create_gpu_machine_success(self):
        with patch("click.echo") as mock_print:
            self.machine_commands.create("GPU", "test-machine", "g4dn.xlarge")
            mock_print.assert_any_call("Machine created successfully. Details:")
            mock_print.assert_any_call(
                json.dumps(
                    self.mock_instance.create_gpu_machine.return_value["data"], indent=2
                )
            )

    def test_create_fpga_machine_success(self):
        with patch("click.echo") as mock_print:
            self.machine_commands.create("FPGA", "test-machine", "f1.2xlarge")
            mock_print.assert_any_call("Machine created successfully. Details:")
            mock_print.assert_any_call(
                json.dumps(
                    self.mock_instance.create_fpga_machine.return_value["data"],
                    indent=2,
                )
            )

    def test_create_cpu_machine_success(self):
        with patch("click.echo") as mock_print:
            self.machine_commands.create("CPU", "test-machine", "t2.micro")
            mock_print.assert_any_call("Machine created successfully. Details:")
            mock_print.assert_any_call(
                json.dumps(
                    self.mock_instance.create_cpu_machine.return_value["data"], indent=2
                )
            )

    def test_create_gpu_machine_failure(self):
        self.mock_instance.create_gpu_machine.return_value = {"success": False}
        with patch("click.echo") as mock_print:
            self.machine_commands.create("GPU", "test-machine", "g4dn.xlarge")
            mock_print.assert_called_with(
                "Failed to create machine. Check machine name and type and try again."
            )

    def test_create_fpga_machine_failure(self):
        self.mock_instance.create_fpga_machine.return_value = {"success": False}
        with patch("click.echo") as mock_print:
            self.machine_commands.create("FPGA", "test-machine", "f1.2xlarge")
            mock_print.assert_called_with(
                "Failed to create machine. Check machine name and type and try again."
            )

    def test_create_cpu_machine_failure(self):
        self.mock_instance.create_cpu_machine.return_value = {"success": False}
        with patch("click.echo") as mock_print:
            self.machine_commands.create("CPU", "test-machine", "t2.micro")
            mock_print.assert_called_with(
                "Failed to create machine. Check machine name and type and try again."
            )

    def test_create_machine_invalid_hardware_type(self):
        with patch("click.echo") as mock_print:
            self.machine_commands.create("INVALID", "test-machine", "t2.micro")
            mock_print.assert_called_with("Invalid hardware type.")

    def test_pull_gpu_model_success(self):
        with patch("click.echo") as mock_print:
            self.machine_commands.pull_model("GPU", "test123", "test-model")
            mock_print.assert_called_with("Model test-model pulled successfully.")

    def test_pull_cpu_model_success(self):
        with patch("click.echo") as mock_print:
            self.machine_commands.pull_model("CPU", "test123", "test-model")
            mock_print.assert_called_with("Model test-model pulled successfully.")

    def test_pull_fpga_model_not_supported(self):
        with patch("click.secho") as mock_print:
            self.machine_commands.pull_model("FPGA", "test123", "test-model")
            mock_print.assert_called_with(
                "FPGA pull model not supported yet.", fg="yellow"
            )

    def test_pull_gpu_model_failure(self):
        self.mock_instance.pull_gpu_model.return_value = {"success": False}
        with patch("click.echo") as mock_print:
            self.machine_commands.pull_model("GPU", "test123", "test-model")
            mock_print.assert_called_with(
                "Failed to pull model. Check machine ID and model name and try again."
            )

    def test_pull_cpu_model_failure(self):
        self.mock_instance.pull_cpu_model.return_value = {"success": False}
        with patch("click.echo") as mock_print:
            self.machine_commands.pull_model("CPU", "test123", "test-model")
            mock_print.assert_called_with(
                "Failed to pull model. Check machine ID and model name and try again."
            )

    def test_pull_model_invalid_hardware_type(self):
        with patch("click.echo") as mock_print:
            self.machine_commands.pull_model("INVALID", "test123", "test-model")
            mock_print.assert_called_with("Invalid hardware type.")

    def test_delete_gpu_model_success(self):
        with patch("click.echo") as mock_print:
            self.machine_commands.delete_machine_model("GPU", "test123", "test-model")
            mock_print.assert_called_with("Model test-model deleted successfully.")

    def test_delete_cpu_model_success(self):
        with patch("click.echo") as mock_print:
            self.machine_commands.delete_machine_model("CPU", "test123", "test-model")
            mock_print.assert_called_with("Model test-model deleted successfully.")

    def test_delete_fpga_model_not_supported(self):
        with patch("click.secho") as mock_print:
            self.machine_commands.delete_machine_model("FPGA", "test123", "test-model")
            mock_print.assert_called_with(
                "FPGA delete model not supported yet.", fg="yellow"
            )

    def test_delete_gpu_model_failure(self):
        self.mock_instance.delete_gpu_model.return_value = {"success": False}
        with patch("click.echo") as mock_print:
            self.machine_commands.delete_machine_model("GPU", "test123", "test-model")
            mock_print.assert_called_with(
                "Failed to delete model. Check machine ID and model name and try again."
            )

    def test_delete_cpu_model_failure(self):
        self.mock_instance.delete_cpu_model.return_value = {"success": False}
        with patch("click.echo") as mock_print:
            self.machine_commands.delete_machine_model("CPU", "test123", "test-model")
            mock_print.assert_called_with(
                "Failed to delete model. Check machine ID and model name and try again."
            )

    def test_delete_model_invalid_hardware_type(self):
        with patch("click.echo") as mock_print:
            self.machine_commands.delete_machine_model(
                "INVALID", "test123", "test-model"
            )
            mock_print.assert_called_with("Invalid hardware type.")

    def test_get_gpu_inference_url_success(self):
        with patch("click.echo") as mock_print:
            self.machine_commands.get_inference_url("GPU", "test123")
            mock_print.assert_called_with("Inference URL: http://gpu-inference-url")

    def test_get_cpu_inference_url_success(self):
        with patch("click.echo") as mock_print:
            self.machine_commands.get_inference_url("CPU", "test123")
            mock_print.assert_called_with("Inference URL: http://cpu-inference-url")

    def test_get_fpga_inference_url_success(self):
        self.mock_instance.get_fpga_inference_url.return_value = {
            "success": True,
            "data": {"inference_url": "http://fpga-inference-url"},
        }
        with patch("click.echo") as mock_print:
            self.machine_commands.get_inference_url("FPGA", "test123")
            mock_print.assert_called_with("Inference URL: http://fpga-inference-url")

    def test_get_inference_url_invalid_hardware_type(self):
        with patch("click.echo") as mock_print:
            self.machine_commands.get_inference_url("INVALID", "test123")
            mock_print.assert_called_with("Invalid hardware type.")

    def test_get_cpu_inference_url_failure(self):
        self.mock_instance.get_cpu_inference_url.return_value = {"success": False}
        with patch("click.echo") as mock_print:
            self.machine_commands.get_inference_url("CPU", "test123")
            mock_print.assert_called_with(
                "Failed to get inference URL. Check machine ID and try again."
            )

    def test_get_fpga_inference_url_failure(self):
        self.mock_instance.get_fpga_inference_url.return_value = {"success": False}
        with patch("click.echo") as mock_print:
            self.machine_commands.get_inference_url("FPGA", "test123")
            mock_print.assert_called_with(
                "Failed to get inference URL. Check machine ID and try again."
            )

    def test_get_gpu_inference_url_failure(self):
        self.mock_instance.get_gpu_inference_url.return_value = {"success": False}
        with patch("click.echo") as mock_print:
            self.machine_commands.get_inference_url("GPU", "test123")
            mock_print.assert_called_with(
                "Failed to get inference URL. Check machine ID and try again."
            )

    def test_list_machines_success(self):
        self.mock_instance.list_user_machines.return_value = {
            "success": True,
            "data": [
                {
                    "machine_id": "test123",
                    "machine_name": "test-machine",
                    "machine_type": "g4dn.xlarge",
                }
            ],
        }
        with patch("click.echo") as mock_print:
            self.machine_commands.list()
            mock_print.assert_any_call("Machines:")
            mock_print.assert_any_call(
                json.dumps(
                    self.mock_instance.list_user_machines.return_value["data"][0],
                    indent=2,
                )
            )

    def test_list_machines_no_machines(self):
        self.mock_instance.list_user_machines.return_value = {
            "success": True,
            "data": [],
        }
        with patch("click.echo") as mock_print:
            self.machine_commands.list()
            mock_print.assert_called_with("No machines to list.")

    def test_list_machines_failure(self):
        self.mock_instance.list_user_machines.return_value = {"success": False}
        with patch("click.echo") as mock_print:
            self.machine_commands.list()
            mock_print.assert_called_with("Failed to retrieve list of machines.")

    def test_stop_machine_success(self):
        self.mock_instance.stop_machine.return_value = {
            "success": True,
            "data": {"message": "Machine stopped successfully"},
        }
        with patch("click.echo") as mock_print:
            self.machine_commands.stop("test123")
            mock_print.assert_called_with("Machine stopped successfully")

    def test_stop_machine_failure(self):
        self.mock_instance.stop_machine.return_value = {"success": False}
        with patch("click.echo") as mock_print:
            self.machine_commands.stop("test123")
            mock_print.assert_called_with(
                "Failed to stop machine. Check machine ID and try again."
            )

    def test_start_machine_success(self):
        self.mock_instance.start_machine.return_value = {
            "success": True,
            "data": {"message": "Machine started successfully"},
        }
        with patch("click.echo") as mock_print:
            self.machine_commands.start("test123")
            mock_print.assert_called_with("Machine started successfully")

    def test_start_machine_failure(self):
        self.mock_instance.start_machine.return_value = {"success": False}
        with patch("click.echo") as mock_print:
            self.machine_commands.start("test123")
            mock_print.assert_called_with(
                "Failed to start machine. Check machine ID and try again."
            )

    def test_terminate_machine_success(self):
        self.mock_instance.terminate_machine.return_value = {
            "success": True,
            "data": {"message": "Machine terminated successfully"},
        }
        with patch("click.echo") as mock_print:
            self.machine_commands.terminate("test123")
            mock_print.assert_called_with("Machine terminated successfully")

    def test_terminate_machine_failure(self):
        self.mock_instance.terminate_machine.return_value = {"success": False}
        with patch("click.echo") as mock_print:
            self.machine_commands.terminate("test123")
            mock_print.assert_called_with(
                "Failed to terminate machine. Check machine ID and try again."
            )

    def test_get_details_success(self):
        self.mock_instance.get_machine.return_value = {
            "success": True,
            "data": {
                "machine_id": "test123",
                "machine_name": "test-machine",
                "machine_type": "g4dn.xlarge",
            },
        }
        with patch("click.echo") as mock_print:
            self.machine_commands.get_details("test123")
            mock_print.assert_any_call("Machine test123 details:")
            mock_print.assert_any_call(
                json.dumps(
                    self.mock_instance.get_machine.return_value["data"], indent=2
                )
            )

    def test_get_details_failure(self):
        self.mock_instance.get_machine.return_value = {"success": False}
        with patch("click.echo") as mock_print:
            self.machine_commands.get_details("test123")
            mock_print.assert_called_with(
                "Failed to get machine. Check machine ID and try again."
            )


class TestMachineCommandsInvoke(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    @patch("src.commands.machine.MachineCommands.create")
    def test_create_success_command(self, mock_create):
        result = self.runner.invoke(
            machine,
            [
                "create",
                "GPU",
                "--machine-name",
                "test-machine",
                "--machine-type",
                "g4dn.xlarge",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        mock_create.assert_called_once_with("GPU", "test-machine", "g4dn.xlarge")

    @patch("src.commands.machine.MachineCommands.create")
    def test_create_failure_command(self, mock_create):
        mock_create.return_value = -1
        result = self.runner.invoke(
            machine,
            [
                "create",
                "GPU",
                "--machine-name",
                "test-machine",
                "--machine-type",
                "t2.micro",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        mock_create.assert_not_called()

    @patch("src.commands.machine.MachineCommands.pull_model")
    def test_pull_model_command(self, mock_pull_model):
        with patch(
            "builtins.open",
            unittest.mock.mock_open(
                read_data='[{"name": "test-model", "available": {"GPU": true}}]'
            ),
        ):
            result = self.runner.invoke(
                machine,
                [
                    "pull-model",
                    "GPU",
                    "--machine-id",
                    "test123",
                    "--model-name",
                    "test-model",
                ],
            )
        self.assertEqual(result.exit_code, 0)
        mock_pull_model.assert_called_once_with("GPU", "test123", "test-model")

    @patch("src.commands.machine.MachineCommands.pull_model")
    def test_pull_model_failure_command(self, mock_pull_model):
        with patch(
            "builtins.open",
            unittest.mock.mock_open(
                read_data='[{"name": "test-model", "available": {"GPU": false}}]'
            ),
        ):
            result = self.runner.invoke(
                machine,
                [
                    "pull-model",
                    "GPU",
                    "--machine-id",
                    "test123",
                    "--model-name",
                    "test-model",
                ],
            )
        self.assertEqual(result.exit_code, 0)
        mock_pull_model.assert_not_called()

    @patch("src.commands.machine.MachineCommands.delete_machine_model")
    def test_delete_model_command(self, mock_delete_model):
        result = self.runner.invoke(
            machine,
            [
                "delete-model",
                "GPU",
                "--machine-id",
                "test123",
                "--model-name",
                "test-model",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        mock_delete_model.assert_called_once_with("GPU", "test123", "test-model")

    @patch("src.commands.machine.MachineCommands.get_inference_url")
    def test_infer_url_command(self, mock_get_inference_url):
        result = self.runner.invoke(
            machine,
            [
                "infer-url",
                "GPU",
                "--machine-id",
                "test123",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        mock_get_inference_url.assert_called_once_with("GPU", "test123")

    @patch("src.commands.machine.MachineCommands.list")
    def test_list_command(self, mock_list):
        result = self.runner.invoke(machine, ["list"])
        self.assertEqual(result.exit_code, 0)
        mock_list.assert_called_once()

    @patch("src.commands.machine.MachineCommands.stop")
    def test_stop_command(self, mock_stop):
        result = self.runner.invoke(
            machine,
            [
                "stop",
                "--machine-id",
                "test123",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        mock_stop.assert_called_once_with("test123")

    @patch("src.commands.machine.MachineCommands.start")
    def test_start_command(self, mock_start):
        result = self.runner.invoke(
            machine,
            [
                "start",
                "--machine-id",
                "test123",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        mock_start.assert_called_once_with("test123")

    @patch("src.commands.machine.MachineCommands.terminate")
    def test_terminate_command(self, mock_terminate):
        result = self.runner.invoke(
            machine,
            [
                "terminate",
                "--machine-id",
                "test123",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        mock_terminate.assert_called_once_with("test123")

    @patch("src.commands.machine.MachineCommands.get_details")
    def test_details_command(self, mock_get_details):
        result = self.runner.invoke(
            machine,
            [
                "details",
                "--machine-id",
                "test123",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        mock_get_details.assert_called_once_with("test123")
