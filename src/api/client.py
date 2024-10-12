import requests
from src.config.settings import API_BASE_URL
from src.utils.password_handler import PasswordHandler

SERVICE_NAME = "quack"


class APIClient:
    def __init__(self, base_url=API_BASE_URL):
        self.base_url = base_url
        self.password_handler = PasswordHandler(SERVICE_NAME)
        self.session = requests.Session()
        self.api_key = self.get_api_key()
        self.access_token = self.get_access_token()

    def _make_request(self, method, endpoint, data=None, params=None, headers=None):
        url = f"{self.base_url}/{endpoint}"
        headers = headers or {}

        if self.api_key:
            headers["X-API-Key"] = self.api_key
        elif not self.api_key and self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"

        response = self.session.request(
            method,
            url,
            json=data if endpoint != "auth" else None,
            data=data if endpoint == "auth" else None,
            params=params,
            headers=headers,
        )
        response.raise_for_status()
        return response.json()

    def get(self, endpoint, params=None, headers=None):
        return self._make_request("GET", endpoint, params=params, headers=headers)

    def post(self, endpoint, data=None, params=None, headers=None):
        return self._make_request(
            "POST", endpoint, data=data, params=params, headers=headers
        )

    def put(self, endpoint, data=None, params=None, headers=None):
        return self._make_request(
            "PUT", endpoint, data=data, params=params, headers=headers
        )

    def delete(self, endpoint, data=None, params=None, headers=None):
        return self._make_request(
            "DELETE", endpoint, data=data, params=params, headers=headers
        )

    def set_access_token(self, token):
        self.access_token = token
        self.password_handler.set_password("access_token", token)

    def get_access_token(self):
        return self.password_handler.get_password("access_token")

    def clear_access_token(self):
        if (
            self.access_token is None
            and self.password_handler.get_password("access_token") is None
        ):
            return False
        self.access_token = None
        return self.password_handler.delete_password("access_token")

    def set_api_key(self, api_key):
        self.api_key = api_key
        self.password_handler.set_password("api_key", api_key)

    def get_api_key(self):
        return self.password_handler.get_password("api_key")

    def clear_api_key(self):
        if (
            self.api_key is None
            and self.password_handler.get_password("api_key") is None
        ):
            return False
        self.api_key = None
        return self.password_handler.delete_password("api_key")
