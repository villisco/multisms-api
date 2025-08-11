import requests

from flask_openapi3 import APIBlueprint, Tag
from flask import current_app as app

from config import AuthSecurity
from application.utils.rate_limiter import limiter
from application.services.telia_api import TeliaMultiSmsAPI
from application.core.telia_payload import TeliaPayload
from application.schemas.api.api_post_body import PostBodySms
from application.schemas.api.api_responses import ApiSuccessResponse, ApiErrorResponse

bp = APIBlueprint("post_sms", __name__)
tags = Tag(name="SMS")

@bp.post(
        "/sms",
        summary="Send SMS to receivers list",
        tags=[tags],
        responses={
            200: ApiSuccessResponse,
            207: ApiSuccessResponse,
            400: ApiErrorResponse,
            401: ApiErrorResponse,
            413: ApiErrorResponse,
            500: ApiErrorResponse,
            502: ApiErrorResponse,
            504: ApiErrorResponse
        },
        security=AuthSecurity.security,
)
@limiter.limit("5/minute")
def post_sms(body: PostBodySms) -> requests.Response:
    app.logger.debug("[sms] Received POST request with post_body: %s" % body)

    telia_payload = TeliaPayload()
    telia_api = TeliaMultiSmsAPI(
        app.config['TELIA_URL'],
        app.config['TELIA_USER'],
        app.config['TELIA_PW']
    )

    sms_messages = telia_payload.prepare_payload(body.receiver_groups, body.sms_text)
    api_response = telia_api.post_sms(sms_messages)

    return api_response