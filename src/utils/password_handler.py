import keyring


class PasswordHandler:
    def __init__(self, service_name):
        self.service_name = service_name

    def set_password(self, key, value):
        keyring.set_password(self.service_name, key, value)

    def get_password(self, key):
        return keyring.get_password(self.service_name, key)

    def delete_password(self, key):
        try:
            keyring.delete_password(self.service_name, key)
            return True
        except keyring.errors.PasswordDeleteError:
            return False
