from typing import Any


def format_response(success: bool, message: str, data: Any = None) -> dict[str, Any]:
    response = {
        "success": success,
        "message": message,
    }
    if data is not None:
        response["data"] = data
    return response

