import requests
from ..config.settings import API_BASE_URL
from .auth_api import AuthAPI
# Import other API modules as needed


class APIClient:
    def __init__(self, base_url=API_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.access_token = None

        # Initialize API modules
        self.auth = AuthAPI(self)
        # Initialize other API modules as needed
        # self.users = UsersAPI(self)
        # self.products = ProductsAPI(self)

    def _make_request(self, method, endpoint, data=None, params=None):
        url = f"{self.base_url}/{endpoint}"
        headers = {}
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        response = self.session.request(
            method, url, json=data, params=params, headers=headers
        )
        response.raise_for_status()
        return response.json()

    def get(self, endpoint, params=None):
        return self._make_request("GET", endpoint, params=params)

    def post(self, endpoint, data=None, headers=None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()
        return response

    def put(self, endpoint, data):
        return self._make_request("PUT", endpoint, data=data)

    def delete(self, endpoint):
        return self._make_request("DELETE", endpoint)

    def set_access_token(self, token):
        print(token)
        self.access_token = token
