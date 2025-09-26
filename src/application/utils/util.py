import requests
from pydantic import BaseModel, ValidationError
from flask import current_app as app

from application.utils.exceptions import ApiException, ApiError
from application.schemas.services.telia_responses import TeliaSuccessResponse

def pydantic_model_to_dict(model_instance: BaseModel) -> dict:
    """
    pydantic model can't be passed directly into requests
    """
    return model_instance.model_dump(by_alias=True)

def response_to_pydantic_model(response: requests.Response, schema: TeliaSuccessResponse) -> TeliaSuccessResponse:
    """
    Acts as an validator for the response (if it matches predefined pydantic schema)
    """
    try:
        return schema(**response.json())
    except (ValueError, ValidationError) as parse_err:
        app.logger.error("Failed to parse Telia API response into \"%s\" schema: %s" % (schema.__name__, parse_err))
        raise ApiException(
            ApiError.TELIA_INVALID_RESPONSE_FORMAT,
            status_code=502,
            details={"Response text": response.text[:200]}  # optional
        )

def _get_config_envvars() -> dict[str, str]:
    base_config = {}

    # selected envvars only
    base_config['LOG_LEVEL_APP'] = app.config['LOG_LEVEL_APP']
    base_config['TELIA_URL'] = app.config['TELIA_URL']
    base_config['SMS_SENDER'] = app.config['SMS_SENDER']
    base_config['SMS_MAX_RECEIVERS'] = app.config['SMS_MAX_RECEIVERS']

    return base_config

def _get_config_groups() -> dict:
    groups = app.config["receiver_groups"]
    groups = [g.model_dump() for g in groups]

    return groups

def loaded_config() -> dict:
    config = {}
    
    config["env_vars"] = _get_config_envvars()
    config["receiver_groups"] = _get_config_groups()

    return config