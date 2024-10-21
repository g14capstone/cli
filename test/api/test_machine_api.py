import unittest
from unittest.mock import patch

from src.api.api_client import APIClient
from src.api.machine_api import MachineAPI


class TestMachineAPI(unittest.TestCase):
    def setUp(self):
        self.api = MachineAPI()

    @patch.object(APIClient, "post")
    def test_create_machine(self, mock_post):
        mock_post.return_value = {"status": "success"}
        response = self.api.create_machine("test_machine", "type_a")
        self.assertEqual(response, {"success": True, "data": {"status": "success"}})
        mock_post.assert_called_with(
            "machine", data={"machine_name": "test_machine", "machine_type": "type_a"}
        )

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
        mock_get.assert_called_with("machines/123")

    @patch.object(APIClient, "post")
    def test_start_machine(self, mock_post):
        mock_post.return_value = {"status": "started"}
        response = self.api.start_machine("123")
        self.assertEqual(response, {"success": True, "data": {"status": "started"}})
        mock_post.assert_called_with("machines/start/123")

    @patch.object(APIClient, "post")
    def test_stop_machine(self, mock_post):
        mock_post.return_value = {"status": "stopped"}
        response = self.api.stop_machine("123")
        self.assertEqual(response, {"success": True, "data": {"status": "stopped"}})
        mock_post.assert_called_with("machines/stop/123")

    @patch.object(APIClient, "delete")
    def test_terminate_machine(self, mock_delete):
        mock_delete.return_value = {"status": "terminated"}
        response = self.api.terminate_machine("123")
        self.assertEqual(response, {"success": True, "data": {"status": "terminated"}})
        mock_delete.assert_called_with("machines/123")
