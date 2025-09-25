from flask_openapi3 import APIBlueprint, Tag
from flask import jsonify

from application.schemas.api.api_responses import HealthResponse

bp = APIBlueprint('root_blueprint', __name__)
tags = Tag(name="Monitoring")

@bp.get(
    "/health", 
    summary="Check if application is up", 
    tags=[tags],
    responses={
        200: HealthResponse
    }
)
def get_health():
    return jsonify({"status": "up"}), 200