import requests

from flask_openapi3 import APIBlueprint, Tag
from flask import jsonify
from flask import current_app as app

from config import AuthSecurity
from application.utils.rate_limiter import limiter
from application.services.telia_api import TeliaMultiSmsAPI
from application.core.telia_payload import TeliaPayload
from application.core.alert_payload import AlertmanagerPayload
from application.schemas.api.api_responses import ApiSuccessResponse, ApiErrorResponse
from application.schemas.api.api_post_body import AlertmanagerWebhookPayload
from application.schemas.api.api_params import UrlRequiredParams
from application.utils.exceptions import ApiException, ApiError

bp = APIBlueprint("post_alert", __name__)
tags = Tag(name="SMS")

@bp.post(
        "/webhooks/alertmanager",
        summary="Alertmanager webhook compatible endpoint",
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
def post_alert(query: UrlRequiredParams, body: AlertmanagerWebhookPayload) -> requests.Response:
    app.logger.debug("[sms-alertmanager] Received POST request with post_body: %s" % body)

    telia_payload = TeliaPayload()
    alert_payload = AlertmanagerPayload()
    telia_api = TeliaMultiSmsAPI(
        app.config['TELIA_URL'],
        app.config['TELIA_USER'],
        app.config['TELIA_PW']
    )

    sms_groups = alert_payload.receivers_string_to_list(query.receiver_groups)
    sms_text = alert_payload.parse_alert_to_smstext(body)
    sms_messages = telia_payload.prepare_payload(sms_groups, sms_text)

    api_response = telia_api.post_sms(sms_messages)

    return api_response