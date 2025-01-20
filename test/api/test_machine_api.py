import unittest
from unittest.mock import patch

from src.api.api_client import APIClient
from src.api.machine_api import MachineAPI


class TestMachineAPI(unittest.TestCase):
    def setUp(self):
        self.api = MachineAPI()

    @patch.object(APIClient, "post")
    def test_create_fpga_machine(self, mock_post):
        mock_post.return_value = {"status": "success"}
        response = self.api.create_fpga_machine("test_fpga", "type_a")
        self.assertEqual(response["data"], {"status": "success"})
        mock_post.assert_called_with(
            "machine/fpga",
            data={"machine_name": "test_fpga", "machine_type": "type_a"},
        )

    @patch.object(APIClient, "get")
    def test_get_fpga_inference_url(self, mock_get):
        mock_get.return_value = {"inference_url": "http://example.com"}
        response = self.api.get_fpga_inference_url("123")
        self.assertEqual(response["data"], {"inference_url": "http://example.com"})
        mock_get.assert_called_with("machine/fpga/123/inference_url")

    @patch.object(APIClient, "post")
    def test_create_gpu_machine(self, mock_post):
        mock_post.return_value = {"status": "success"}
        response = self.api.create_gpu_machine("test_gpu", "type_b")
        self.assertEqual(response["data"], {"status": "success"})
        mock_post.assert_called_with(
            "machine/gpu",
            data={"machine_name": "test_gpu", "machine_type": "type_b"},
        )

    @patch.object(APIClient, "post")
    def test_pull_gpu_model(self, mock_post):
        mock_post.return_value = {"status": "pulled"}
        response = self.api.pull_gpu_model("123", "model_a")
        self.assertEqual(response["data"], {"status": "pulled"})
        mock_post.assert_called_with(
            "machine/gpu/pull_model",
            data={"machine_id": "123", "model_name": "model_a"},
        )

    @patch.object(APIClient, "delete")
    def test_delete_gpu_model(self, mock_delete):
        mock_delete.return_value = {"status": "deleted"}
        response = self.api.delete_gpu_model("123", "model_a")
        self.assertEqual(response["data"], {"status": "deleted"})
        mock_delete.assert_called_with(
            "machine/gpu/model",
            data={"machine_id": "123", "model_name": "model_a"},
        )

    @patch.object(APIClient, "get")
    def test_get_gpu_inference_url(self, mock_get):
        mock_get.return_value = {"inference_url": "http://example.com"}
        response = self.api.get_gpu_inference_url("123")
        self.assertEqual(response["data"], {"inference_url": "http://example.com"})
        mock_get.assert_called_with("machine/gpu/123/inference_url")

    @patch.object(APIClient, "post")
    def test_create_cpu_machine(self, mock_post):
        mock_post.return_value = {"status": "success"}
        response = self.api.create_cpu_machine("test_cpu", "type_c")
        self.assertEqual(response["data"], {"status": "success"})
        mock_post.assert_called_with(
            "machine/cpu",
            data={"machine_name": "test_cpu", "machine_type": "type_c"},
        )

    @patch.object(APIClient, "post")
    def test_pull_cpu_model(self, mock_post):
        mock_post.return_value = {"status": "pulled"}
        response = self.api.pull_cpu_model("123", "model_b")
        self.assertEqual(response["data"], {"status": "pulled"})
        mock_post.assert_called_with(
            "machine/cpu/pull_model",
            data={"machine_id": "123", "model_name": "model_b"},
        )

    @patch.object(APIClient, "delete")
    def test_delete_cpu_model(self, mock_delete):
        mock_delete.return_value = {"status": "deleted"}
        response = self.api.delete_cpu_model("123", "model_b")
        self.assertEqual(response["data"], {"status": "deleted"})
        mock_delete.assert_called_with(
            "machine/cpu/model",
            data={"machine_id": "123", "model_name": "model_b"},
        )

    @patch.object(APIClient, "get")
    def test_get_cpu_inference_url(self, mock_get):
        mock_get.return_value = {"inference_url": "http://example.com"}
        response = self.api.get_cpu_inference_url("123")
        self.assertEqual(response["data"], {"inference_url": "http://example.com"})
        mock_get.assert_called_with("machine/cpu/123/inference_url")

    @patch.object(APIClient, "get")
    def test_list_user_machines(self, mock_get):
        mock_get.return_value = {"machines": []}
        response = self.api.list_user_machines()
        self.assertEqual(response, {"success": True, "data": {"machines": []}})
        mock_get.assert_called_with("machines")

    @patch.object(APIClient, "get")
    def test_get_machine(self, mock_get):
        mock_get.return_value = {"machine_id": "123"}
        response = self.api.get_machine("123")
        self.assertEqual(response, {"success": True, "data": {"machine_id": "123"}})
        mock_get.assert_called_with("machine/123")

    @patch.object(APIClient, "post")
    def test_start_machine(self, mock_post):
        mock_post.return_value = {"status": "started"}
        response = self.api.start_machine("123")
        self.assertEqual(response, {"success": True, "data": {"status": "started"}})
        mock_post.assert_called_with("machine/start/123")

    @patch.object(APIClient, "post")
    def test_stop_machine(self, mock_post):
        mock_post.return_value = {"status": "stopped"}
        response = self.api.stop_machine("123")
        self.assertEqual(response, {"success": True, "data": {"status": "stopped"}})
        mock_post.assert_called_with("machine/stop/123")

    @patch.object(APIClient, "delete")
    def test_terminate_machine(self, mock_delete):
        mock_delete.return_value = {"status": "terminated"}
        response = self.api.terminate_machine("123")
        self.assertEqual(response, {"success": True, "data": {"status": "terminated"}})
        mock_delete.assert_called_with("machine/123")
