from flask_openapi3 import APIBlueprint, Tag
from flask import Response, render_template

from application.utils.util import loaded_config

bp = APIBlueprint('index_blueprint', __name__)
tags = Tag(name="UI")

@bp.get(
    "/",
    summary="View Current Configuration (xhtml)", 
    tags=[tags]
)
def get_index():
  xml = render_template("index.xhtml", config=loaded_config())
  return Response(xml, content_type="application/xhtml+xml; charset=utf-8")