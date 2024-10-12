from typing import Dict, List, Union
from datetime import datetime
from src.utils.helpers.validity_enum import ValidityEnum
from src.utils.helpers.handle_api_errors import handle_api_errors


class AuthAPI:
    def __init__(self, client):
        self.client = client

    @handle_api_errors
    def login(self, username: str, password: str) -> Dict[str, str]:
        data = {
            "username": username,
            "password": password,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = self.client.post("auth", data=data, headers=headers)
        print(response)
        if "access_token" in response:
            self.client.set_access_token(response["access_token"])
            return "Login successful"
        else:
            raise Exception(f"Failed to login: {response}")

    def logout(self) -> bool:
        return self.client.clear_access_token()
    
    def set_api_key(self, api_key: str) -> None:
        self.client.set_api_key(api_key)

    def clear_api_key(self) -> bool:
        return self.client.clear_api_key()

    @handle_api_errors
    def create_api_key(self, validity: ValidityEnum) -> str:
        return self.client.get(f"auth/api_key/{validity.value}")

    @handle_api_errors
    def list_api_keys(self) -> List[Dict[str, Union[str, datetime]]]:
        return self.client.get("auth/api_keys")

    @handle_api_errors
    def delete_api_key(self, token: str) -> str:
        return self.client.delete(f"auth/api_key/{token}")

