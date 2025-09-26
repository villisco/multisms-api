from flask_openapi3 import APIBlueprint, Tag
from flask import jsonify, make_response
from flask import current_app as app

from application.utils.util import loaded_config
from application.schemas.api.api_responses import ApiConfigResponse, ApiErrorResponse

bp = APIBlueprint('config_blueprint', __name__)
tags = Tag(name="Monitoring")

@bp.get(
    "/config", 
    summary="Application configuration", 
    tags=[tags],
    responses={
        200: ApiConfigResponse,
        500: ApiErrorResponse,
    }
)
def get_config():
    return make_response(jsonify(loaded_config()), 200)