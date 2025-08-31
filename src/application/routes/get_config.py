from flask_openapi3 import APIBlueprint, Tag
from flask import jsonify, make_response
from flask import current_app as app

from application.schemas.api.api_responses import ApiConfigResponse, ApiErrorResponse

bp = APIBlueprint('config_blueprint', __name__)
tags = Tag(name="Config")

@bp.get(
    "/groups", 
    summary="Currently configured SMS receiver groups", 
    tags=[tags],
    responses={
        200: ApiConfigResponse,
        500: ApiErrorResponse,
    }
)
def get_groups():
    groups = app.config["receiver_groups"]
    groups_list = [g.model_dump() for g in groups]

    payload = {"receiver_groups": groups_list}

    return make_response(jsonify(payload), 200)