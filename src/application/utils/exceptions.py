class ApiException(Exception):
    def __init__(self, error: dict, status_code: int = 400, details: dict = None):
        self.code = error.get("code", "UNKNOWN_ERROR")
        self.message = error.get("message", "Unknown error occurred")
        self.status_code = status_code
        self.details = details or {}

class ApiError():
    AUTH_BASIC_REQUIRED = {
        "code": "AUTH_BASIC_REQUIRED",
        "message": "Basic Authorization is required"
    }
    UNKNOWN_RECEIVER_GROUP = {
        "code": "UNKNOWN_RECEIVER_GROUP",
        "message": "Unknown receiver_group was used in request"
    }
    TELIA_CONNECTION_FAILED = {
        "code": "TELIA_CONNECTION_FAILED",
        "message": "Could not connect to Telia SMS API."
    }
    TELIA_TIMEOUT = {
        "code": "TELIA_TIMEOUT",
        "message": "The SMS provider did not respond in time. Please try again later."
    }
    TELIA_SERVICE_ERROR = {
        "code": "TELIA_SERVICE_ERROR",
        "message": "An unexpected error occurred in the SMS provider service."
    }
    TELIA_INVALID_RESPONSE_FORMAT = {
        "code": "TELIA_INVALID_RESPONSE_FORMAT",
        "message": "Telia service returned an unrecognized response."
    }
    TELIA_BAD_REQUEST = {
        "code": "TELIA_BAD_REQUEST",
        "message": "Telia request input was invalid or malformed."
    }
    TELIA_UNSUCCESSFUL_REQUEST = {
        "code": "TELIA_UNSUCCESSFUL_REQUEST",
        "message": "Telia request was unsuccessful. No SMS messages were sent."
    }
    TELIA_UNHANDLED_ERROR = {
        "code": "TELIA_UNHANDLED_ERROR",
        "message": "Unknown error from Telia."
    }