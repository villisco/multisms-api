from os import environ
from dotenv import load_dotenv

APP_NAME = "multisms-api"
APP_VERSION = "3.1.0"

# load environment variables from ".env" file for local development (if exists)
load_dotenv()

class AuthSecurity:
    basic = {
        "type": "http",
        "scheme": "basic"
    }
    security_schemes = {"basic": basic}
    security = [{"basic": []}]
    secured_endpoints = [
       "/api/v1/sms",
       "/api/v1/webhooks/alertmanager"
    ]

class Config():
  TESTING = False
  # required envvars
  LOG_LEVEL_APP = environ.get('LOG_LEVEL_APP', 'INFO')
  LOG_LEVEL_HTTP = environ.get('LOG_LEVEL_HTTP', 'INFO')
  LOG_LEVEL_GUNICORN = environ.get('LOG_LEVEL_GUNICORN', 'INFO')
  TELIA_URL = environ.get('TELIA_URL')
  TELIA_USER = environ.get('TELIA_USER')
  TELIA_PW = environ.get('TELIA_PW')
  SMS_MAX_RECEIVERS = environ.get('SMS_MAX_RECEIVERS', 600)
  SMS_SENDER = environ.get('SMS_SENDER')
  API_BASIC_AUTH_USER = environ.get('API_BASIC_AUTH_USER')
  API_BASIC_AUTH_PW = environ.get('API_BASIC_AUTH_PW')
  GROUPS_CONFIG_PATH = environ.get('GROUPS_CONFIG_PATH', 'config/receiver_groups.yaml')

class TestConfig(Config):
  TESTING = True
  # required envvars
  LOG_LEVEL_APP = "DEBUG"
  LOG_LEVEL_HTTP = "DEBUG"
  LOG_LEVEL_GUNICORN = "DEBUG"
  TELIA_URL = "not-configured"
  TELIA_USER = "not-configured"
  TELIA_PW = "not-configured"
  SMS_MAX_RECEIVERS = 20
  SMS_SENDER = "37250000000"
  API_BASIC_AUTH_USER = "test1"
  API_BASIC_AUTH_PW = "test1"
  GROUPS_CONFIG_PATH = "tests/fixtures/receiver_groups_fixture.yaml"