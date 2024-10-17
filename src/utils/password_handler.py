import keyring
from typing import Optional


class PasswordHandler:
    def __init__(self, service_name: str):
        self.service_name: str = service_name

    def set_password(self, key: str, value: str) -> None:
        keyring.set_password(self.service_name, key, value)

    def get_password(self, key: str) -> Optional[str]:
        return keyring.get_password(self.service_name, key)

    def delete_password(self, key: str) -> bool:
        try:
            keyring.delete_password(self.service_name, key)
            return True
        except keyring.errors.PasswordDeleteError:
            return False
