import unittest
from unittest.mock import patch, mock_open
from src.api.api_client import APIClient
from src.api.model_file_api import ModelFileAPI


class TestModelFileAPI(unittest.TestCase):
    def setUp(self):
        self.api = ModelFileAPI()

    @patch("builtins.open", new_callable=mock_open, read_data="test data")
    @patch.object(APIClient, "post")
    def test_upload_model_file(self, mock_post, mock_file):
        mock_post.return_value = {"status": "uploaded"}
        response = self.api.upload_model_file("test_model", "123", "test.file")
        self.assertEqual(response, {"success": True, "data": {"status": "uploaded"}})
        mock_post.assert_called_once()
        mock_file.assert_called_with("test.file", "rb")

    @patch.object(APIClient, "get")
    def test_get_model(self, mock_get):
        mock_get.return_value = {"model_id": "123"}
        response = self.api.get_model("123")
        self.assertEqual(response, {"success": True, "data": {"model_id": "123"}})
        mock_get.assert_called_with("models/123")

    @patch.object(APIClient, "get")
    def test_get_all_models(self, mock_get):
        mock_get.return_value = {"models": []}
        response = self.api.get_all_models()
        self.assertEqual(response, {"success": True, "data": {"models": []}})
        mock_get.assert_called_with("models")

    @patch.object(APIClient, "get")
    def test_read_model_file(self, mock_get):
        mock_get.return_value = {"content": "file_content"}
        response = self.api.read_model_file("123", "test.file")
        self.assertEqual(
            response, {"success": True, "data": {"content": "file_content"}}
        )
        mock_get.assert_called_with("models/123/test.file")

    @patch("builtins.open", new_callable=mock_open, read_data="test data")
    @patch.object(APIClient, "put")
    def test_update_model_file(self, mock_put, mock_file):
        mock_put.return_value = {"status": "updated"}
        response = self.api.update_model_file("test_model", "123", "test.file")
        self.assertEqual(response, {"success": True, "data": {"status": "updated"}})
        mock_put.assert_called_once()
        mock_file.assert_called_with("test.file", "rb")

    @patch.object(APIClient, "delete")
    def test_delete_model_file(self, mock_delete):
        mock_delete.return_value = {"status": "deleted"}
        response = self.api.delete_model_file("123", "test.file")
        self.assertEqual(response, {"success": True, "data": {"status": "deleted"}})
        mock_delete.assert_called_with("models/123/test.file")

    @patch.object(APIClient, "delete")
    def test_delete_model(self, mock_delete):
        mock_delete.return_value = {"status": "deleted"}
        response = self.api.delete_model("123")
        self.assertEqual(response, {"success": True, "data": {"status": "deleted"}})
        mock_delete.assert_called_with("models/123")
