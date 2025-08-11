class PartialTestConfigFixture():
  TESTING = True
  # required envvars
  LOG_LEVEL_APP = "DEBUG"
  LOG_LEVEL_HTTP = "DEBUG"
  LOG_LEVEL_GUNICORN = "DEBUG"
  TELIA_URL = "not-configured"
  TELIA_USER = "not-configured"
  TELIA_PW = "not-configured"
  SMS_MAX_RECEIVERS = 600
  SMS_SENDER = "37250000000"
  API_BASIC_AUTH_USER = "test1"
  API_BASIC_AUTH_PW = "test1"
  #GROUPS_CONFIG_PATH = "tests/fixtures/receiver_groups_fixture.yaml" <!--- simulate missing envvar