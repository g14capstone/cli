class AuthAPI:
    def __init__(self, client):
        self.client = client

    def login(self, username, password):
        data = {
            "username": username,
            "password": password,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = self.client.post("auth", data=data, headers=headers)
        response_data = response.json()
        if response.status_code == 200 and "access_token" in response_data:
            self.client.set_access_token(response_data["access_token"])
        else:
            print(f"Failed to login: {response_data}")
        return response_data

    def logout(self):
        return self.client.post("auth/logout", {})

    def refresh_token(self):
        return self.client.post("auth/refresh", {})
