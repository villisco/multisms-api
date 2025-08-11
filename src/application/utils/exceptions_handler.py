from uuid import uuid4
from flask import jsonify, make_response
from werkzeug.exceptions import HTTPException
from application.utils.exceptions import ApiException
from application.schemas.api.api_responses import ApiErrorResponse, MetaInfo
from application.utils.util import pydantic_model_to_dict

def register_api_error_handler(app):
    # Handle custom exceptions
    @app.errorhandler(ApiException)
    def handle_api_error(error):
        error_id = str(uuid4())  # Generate a unique error ID
        app.logger.error(f"[{error_id}] {error.status_code} - {error.message} (code: {error.code})")

        response = ApiErrorResponse(
            id=error_id,
            error=MetaInfo(
                code=error.code,
                message=error.message,
                details=getattr(error, "details", None),
                partial_success=False
            )
        )

        return make_response(jsonify(pydantic_model_to_dict(response)), error.status_code)

    # by default Flask would return 500 errors as html
    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        error_id = str(uuid4())

        if isinstance(error, HTTPException):
            app.logger.warning(f"[{error_id}] HTTPException {error.code}: {error.description}")
            response = ApiErrorResponse(
                id=error_id,
                error=MetaInfo(
                    code=f"HTTP_{error.code}",
                    message=error.description,
                    details=getattr(error, "details", None),
                    partial_success=False
                )
            )
            return make_response(jsonify(pydantic_model_to_dict(response)), error.code)

        app.logger.exception(f"[{error_id}] Unhandled exception: {str(error)}")
        response = ApiErrorResponse(
            id=error_id,
            error=MetaInfo(
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected error occurred.",
                details=getattr(error, "details", None),
                partial_success=False
            )
        )
        return make_response(jsonify(pydantic_model_to_dict(response)), 500)