from typing import Dict
from src.api.api_client import APIClient
from src.utils.helpers.handle_api_errors import handle_api_errors


class MachineAPI:
    def __init__(self):
        self.client = APIClient()

    """FPGA REQUESTS"""

    @handle_api_errors
    def create_fpga_machine(
        self, machine_name: str, machine_type: str
    ) -> Dict[str, str]:
        data = {
            "machine_name": machine_name,
            "machine_type": machine_type,
        }
        response = self.client.post("machine/fpga", data=data)
        return response

    """GPU REQUESTS"""

    @handle_api_errors
    def create_gpu_machine(
        self, machine_name: str, machine_type: str
    ) -> Dict[str, str]:
        data = {
            "machine_name": machine_name,
            "machine_type": machine_type,
        }
        response = self.client.post("machine/gpu", data=data)
        return response

    @handle_api_errors
    def pull_gpu_model(self, machine_id: str, model_name: str) -> Dict[str, str]:
        data = {
            "machine_name": machine_id,
            "machine_type": model_name,
        }
        response = self.client.post("machine/gpu/pull_model", data=data)
        return response

    @handle_api_errors
    def delete_gpu_model(self, machine_id: str, model_name: str) -> Dict[str, str]:
        data = {
            "machine_name": machine_id,
            "machine_type": model_name,
        }
        response = self.client.delete("machine/gpu/model", data=data)
        return response

    @handle_api_errors
    def get_gpu_inference_url(self, machine_id: str) -> Dict[str, str]:
        return self.client.get(f"machine/gpu/{machine_id}/inference_url")

    """CPU REQUESTS"""

    @handle_api_errors
    def create_cpu_machine(
        self, machine_name: str, machine_type: str
    ) -> Dict[str, str]:
        data = {
            "machine_name": machine_name,
            "machine_type": machine_type,
        }
        response = self.client.post("machine/cpu", data=data)
        return response

    @handle_api_errors
    def pull_cpu_model(self, machine_id: str, model_name: str) -> Dict[str, str]:
        data = {
            "machine_name": machine_id,
            "machine_type": model_name,
        }
        response = self.client.post("machine/cpu/pull_model", data=data)
        return response

    @handle_api_errors
    def delete_cpu_model(self, machine_id: str, model_name: str) -> Dict[str, str]:
        data = {
            "machine_name": machine_id,
            "machine_type": model_name,
        }
        response = self.client.delete("machine/cpu/model", data=data)
        return response

    @handle_api_errors
    def get_cpu_inference_url(self, machine_id: str) -> Dict[str, str]:
        return self.client.get(f"machine/cpu/{machine_id}/inference_url")

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
