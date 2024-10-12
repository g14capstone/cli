from typing import Callable
from functools import wraps
from requests.exceptions import HTTPError
from src.utils.helpers.unauthorized_error import UnauthorizedError


def handle_api_errors(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return {"success": True, "data": func(*args, **kwargs)}
        except UnauthorizedError as ue:
            return {
                "success": False,
                "error": "Authentication error",
                "message": str(ue),
            }
        except HTTPError as http_err:
            return {"success": False, "error": "HTTP error", "message": str(http_err)}
        except Exception as err:
            return {"success": False, "error": "Unexpected error", "message": str(err)}

    return wrapper
