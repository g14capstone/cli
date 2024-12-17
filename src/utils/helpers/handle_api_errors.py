from typing import Callable
from functools import wraps
from requests.exceptions import HTTPError


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
        except Exception as err:
            return {"success": False, "error": "Unexpected error", "message": str(err)}

    return wrapper
