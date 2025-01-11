from src.api.api_client import APIClient
from src.utils.helpers.handle_api_errors import handle_api_errors


class UserAPI:
    def __init__(self, client: APIClient):
        self.client = client

    @handle_api_errors
    def register(self, username, email, password):
        data = {
            "user_name": username,
            "email": email,
            "password": password,
        }
        response = self.client.post("user", data=data)
        if "user_id" in response:
            return response
        else:
            raise Exception(f"Failed to register: {response}")
