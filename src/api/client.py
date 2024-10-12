import requests
import keyring
from ..config.settings import API_BASE_URL
from .auth_api import AuthAPI

SERVICE_NAME = "quack"


class APIClient:
    def __init__(self, base_url=API_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.access_token = self.get_access_token()

        # Initialize API modules
        self.auth = AuthAPI(self)

    def _make_request(self, method, endpoint, data=None, params=None, headers=None):
        url = f"{self.base_url}/{endpoint}"
        headers = headers or {}
        if not self.access_token:
            self.access_token = self.get_access_token()
        if self.access_token:
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

    def get(self, endpoint, params=None):
        return self._make_request("GET", endpoint, params=params)

    def post(self, endpoint, data=None, headers=None):
        return self._make_request("POST", endpoint, data=data, headers=headers)

    def put(self, endpoint, data):
        return self._make_request("PUT", endpoint, data=data)

    def delete(self, endpoint):
        return self._make_request("DELETE", endpoint)

    def set_access_token(self, token):
        self.access_token = token
        keyring.set_password(SERVICE_NAME, "access_token", token)

    def get_access_token(self):
        return keyring.get_password(SERVICE_NAME, "access_token")

    def clear_access_token(self):
        if (
            self.access_token is None
            and keyring.get_password(SERVICE_NAME, "access_token") is None
        ):
            return False

        self.access_token = None
        try:
            keyring.delete_password(SERVICE_NAME, "access_token")
        except keyring.errors.PasswordDeleteError:
            pass
        return True
