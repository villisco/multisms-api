from flask_openapi3 import APIBlueprint, Tag
from flask import jsonify, make_response
from flask import current_app as app

from application.utils.util import get_config_groups, get_config_base
from application.schemas.api.api_responses import ApiConfigGroupsResponse, ApiConfigBaseResponse, ApiErrorResponse

bp = APIBlueprint('config_blueprint', __name__)
tags = Tag(name="Monitoring")

@bp.get(
    "/config", 
    summary="Base application configuration", 
    tags=[tags],
    responses={
        200: ApiConfigBaseResponse,
        500: ApiErrorResponse,
    }
)
def get_config():
    return make_response(jsonify(get_config_base()), 200)

@bp.get(
    "/groups", 
    summary="Currently configured SMS receiver groups", 
    tags=[tags],
    responses={
        200: ApiConfigGroupsResponse,
        500: ApiErrorResponse,
    }
)
def get_groups():
    return make_response(jsonify(get_config_groups()), 200)