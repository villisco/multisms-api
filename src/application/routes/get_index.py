from flask_openapi3 import APIBlueprint, Tag
from flask import Response, render_template

from application.utils.util import get_config_groups, get_config_base

bp = APIBlueprint('index_blueprint', __name__)
tags = Tag(name="UI")

@bp.get(
    "/",
    summary="View Current Configuration (xhtml)", 
    tags=[tags]
)
def get_index():
  xml = render_template("index.xhtml", config_base=get_config_base(), config_groups=get_config_groups())
  return Response(xml, content_type="application/xhtml+xml; charset=utf-8")