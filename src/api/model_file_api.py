import os
from typing import Dict

from src.api.api_client import APIClient
from src.utils.helpers.handle_api_errors import handle_api_errors


class ModelFileAPI:
    def __init__(self, client: APIClient):
        self.client = client

    @handle_api_errors
    def upload_model_file(
        self, model_name: str, model_id: str, file_path: str
    ) -> Dict[str, str]:
        with open(file_path, "rb") as file:
            files = {
                "file": (os.path.basename(file_path), file, "application/octet-stream")
            }
            params = {"model_name": model_name, "model_id": model_id}
            return self.client.post("models", params=params, files=files)

    @handle_api_errors
    def get_model(self, model_id: str):
        return self.client.get(f"models/{model_id}")

    @handle_api_errors
    def get_all_models(self):
        return self.client.get("models")

    @handle_api_errors
    def read_model_file(self, model_id: str, file_name: str):
        return self.client.get(f"models/{model_id}/{file_name}")

    @handle_api_errors
    def update_model_file(
        self, model_name: str, model_id: str, file_path: str
    ) -> Dict[str, str]:
        with open(file_path, "rb") as file:
            files = {
                "file": (os.path.basename(file_path), file, "application/octet-stream")
            }
            params = {"model_name": model_name, "model_id": model_id}
            return self.client.put("models", params=params, files=files)

    @handle_api_errors
    def delete_model_file(self, model_id: str, file_name: str):
        return self.client.delete(f"models/{model_id}/{file_name}")

    @handle_api_errors
    def delete_model(self, model_id: str):
        return self.client.delete(f"models/{model_id}")
