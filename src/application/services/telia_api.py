import requests
from typing import List
from uuid import uuid4
from requests.exceptions import ConnectionError, HTTPError, Timeout

from flask import jsonify, make_response
from flask import current_app as app

from application.schemas.services.telia_payload import SmsMessages
from application.schemas.services.telia_responses import TeliaSuccessResponse
from application.schemas.api.api_responses import ApiSuccessResponse, MetaInfo, DataPayload, FailureItem
from application.utils.exceptions import ApiException, ApiError
from application.utils.util import pydantic_model_to_dict, response_to_pydantic_model

class TeliaMultiSmsAPI():
    """
    # https://www.telia.ee/images/documents/juhendid/eng/MultiSMS_manual_eng.pdf (p6.2)
    API restrictions:
    - SMS content text length limit: 1530 characters
    - Receiving troughput: 20 SMS/sec (default)
    - Sending troughput: 50 – 130 SMS/sec (depends on queue length/priority)
    - Sender:
        - can be number (e.g "372...") or alphanumeric (e.g "Telia")
        - "õ" not supported in sender name
        - allowed characters in sender name: "äöü"
        - NB! when sending to non-estonian numbers alphanumeric senders (e.g "Telia") get generally blocked by foreign operators!
    - Recepient numbers:
        - by default permitted numbers starting with "5" and 372 (numbers of Estonian operators)
        - foreign numbers must include country code prefix (e.g 371)
    """
    def __init__(self, base_url = None, user = None, password = None):
        self.base_url = base_url
        self.user = user
        self.password = password

    def _build_api_success_response(self, validated_response: TeliaSuccessResponse, sms_generated_count: int, status_code: int) -> requests.Response:
        meta_info = MetaInfo(
            code="SUCCESS",
            message="All SMS messages have been fully processed",
            partial_success=False
        )

        if not validated_response.allAcceptedSuccessfully:
            meta_info = MetaInfo(
                code="PARTIAL_SUCCESS",
                message="Some SMS messages may not have been fully processed",
                partial_success=True
            )

        failures: List[FailureItem] = [
            FailureItem(
                code="TELIA_UNACCEPTABLE",
                receiver=um.to,
                message=um.errorMessage or "Unknown error"
            )
            for um in validated_response.unacceptableMessages
        ]

        data_payload = DataPayload(
            sms_generated_count = sms_generated_count,
            sms_sent_count = validated_response.acceptedMessagesCount,
            sms_sent_failed_count = validated_response.unacceptableMessagesCount,
            failures = failures
        )
        
        response = ApiSuccessResponse(
            id=uuid4(),
            meta=meta_info,
            data=data_payload
        )

        return make_response(jsonify(pydantic_model_to_dict(response)), status_code)

    def _build_api_response(self, telia_response: requests.Response, sms_generated_count: int) -> requests.Response:     
        if telia_response.status_code >= 400:
            app.logger.debug("telia_status_code: %s" % telia_response.status_code)
            raise ApiException(
                error=ApiError.TELIA_UNSUCCESSFUL_REQUEST,
                status_code=502,
                details={
                    "response_status_code": telia_response.status_code,
                    "response_text": telia_response.json()
                }
            )
    
        validated_response = response_to_pydantic_model(telia_response, TeliaSuccessResponse)
        api_response = self._build_api_success_response(validated_response, sms_generated_count, telia_response.status_code)

        return api_response

    def _post_request(self, payload: dict) -> requests.Response:
        """
        # https://www.telia.ee/images/documents/juhendid/eng/MultiSMS_manual_eng.pdf (p2.2)
        API responses:
        - 200 OK
        - 400 request input was not correct (request could not be processed)
        - 413 unsuccessful request - no messages were sent.
            - Processing request took over 30sec. too many messages?
            - Input message count exceeds the limit (600)
            - Your account throughput limit(20.00 SMS/sec) is not enough to accept all those messages with one HTTP request
        """
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(
                self.base_url + "/sms", 
                auth=(self.user, self.password), # basic auth
                headers=headers, 
                json=payload, 
                verify=True) # tls verify

            app.logger.debug("[_post_request] Telia API response: %s" % response.json())

            # throws an exception on codes 400-599
            response.raise_for_status()

        # NB! raising ApiException() goes trough "exceptions_handler" that sends an ApiErrorResponse() response out
        except ConnectionError as err:
            app.logger.error("Failed to connect to Telia REST API: %s" % err)
            raise ApiException(ApiError.TELIA_CONNECTION_FAILED, status_code=502)

        except Timeout as err:
            app.logger.error("Telia REST API request timed out: %s" % err)
            raise ApiException(ApiError.TELIA_TIMEOUT, status_code=504)

        except Exception as err:
            app.logger.error("Telia REST API unexpected error: %s" % err)
            raise ApiException(ApiError.TELIA_SERVICE_ERROR, status_code=502)

        # HTTP 2xx/3xx
        return response

    def post_sms(self, sms_messages_list: SmsMessages) -> requests.Response:
        payload = pydantic_model_to_dict(sms_messages_list)
        telia_response = self._post_request(payload)
        
        return self._build_api_response(telia_response, len(sms_messages_list.messages))