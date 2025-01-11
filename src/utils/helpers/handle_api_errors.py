from typing import Callable
from functools import wraps
from requests.exceptions import HTTPError, ConnectionError


def handle_api_errors(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return {"success": True, "data": func(*args, **kwargs)}
        except HTTPError as http_err:
            return {
                "success": False,
                "error": "HTTP error",
                "message": str(http_err),
                "status_code": http_err.response.status_code,
                "response": http_err.response.json(),
            }
        except ConnectionError as conn_err:
            return {
                "success": False,
                "error": "Connection refused",
                "message": str(conn_err),
                "response": {"detail": "Connection refused"},
            }
        except Exception as err:
            return {"success": False, "error": "Unexpected error", "message": str(err)}

    return wrapper
