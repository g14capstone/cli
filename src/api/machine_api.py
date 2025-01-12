from typing import Dict
from src.api.api_client import APIClient
from src.utils.helpers.handle_api_errors import handle_api_errors


class MachineAPI:
    def __init__(self):
        self.client = APIClient()

    @handle_api_errors
    def create_machine(self, machine_name: str, machine_type: str) -> Dict[str, str]:
        data = {
            "machine_name": machine_name,
            "machine_type": machine_type,
        }
        response = self.client.post("machine/fpga", data=data)
        return response

    @handle_api_errors
    def list_user_machines(self):
        return self.client.get("machines")

    @handle_api_errors
    def get_machine(self, machine_id: str):
        return self.client.get(f"machine/{machine_id}")

    @handle_api_errors
    def start_machine(self, machine_id: str):
        return self.client.post(f"machine/start/{machine_id}")

    @handle_api_errors
    def stop_machine(self, machine_id: str):
        return self.client.post(f"machine/stop/{machine_id}")

    @handle_api_errors
    def terminate_machine(self, machine_id: str):
        return self.client.delete(f"machine/{machine_id}")
