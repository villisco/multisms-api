# multisms-api

Wrapper REST API for [Telia Multi SMS](https://www.telia.ee/ari/mobiil/mobiili-lisateenused/multisms) REST API.  


API features:
- Alertmanager webhook compatible endpoint for SMS sending
- SMS receiver groups (whitelisting)
- Rate limiting for API endpoints
- Authentication
- Proxy for Telia API (single whitelisted IP needed)

## Development

> NB! Telia MultiSMS API (https://multisms.telia.ee) has IP whitelisting!

Frameworks used:
- [Flask-OpenAPI3](https://luolingchun.github.io/flask-openapi3/v4.x/) ([github repository](https://github.com/luolingchun/flask-openapi3/tree/master/examples))
- [Flask](https://flask.palletsprojects.com) ([github repository](https://github.com/pallets/flask/))
- [pytest](https://docs.pytest.org/en/stable/) ([github repository](https://github.com/pytest-dev/pytest/))

API docs (auto generated):
- http://127.0.0.1:5000/openapi/swagger
- http://127.0.0.1:5000/openapi/openapi.json

### Local environment setup

#### Specific python version install

Debian/Ubuntu:
```
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update 
sudo apt install python3.13 python3.13-venv
```

#### Environment & Packages

Create python venv  
_(if `./src/.venv` does not exist)_
```
cd ./src
python3.13 -m venv .venv
```

Activate venv
```
. .venv/bin/activate
```

Install required packages into venv
```
pip install --upgrade pip
pip install -r requirements.txt
```
> NB! re-run install when `requirements.txt` gets updated!

#### Configuration

Create `./src/.env` file with __required__ environment variables (__local development__):  
```
LOG_LEVEL_APP="INFO"
LOG_LEVEL_HTTP="INFO"
LOG_LEVEL_GUNICORN="INFO"
TELIA_URL="https://multisms.telia.ee"
TELIA_USER=""
TELIA_PW=""
API_BASIC_AUTH_USER="test1"
API_BASIC_AUTH_PW="test1"
SMS_SENDER=""
```
> NB! Use `API_BASIC_AUTH_USER` + `API_BASIC_AUTH_PW` value in Swagger "Authorize".

Create `./src/config/receiver_groups.yaml` with SMS receivers groups (example):
```
receiver_groups:
  - name: test_group1
    description: valid sms senders group
    receivers:
      - 37256000001
      - 37256000002
      - 37256000003
  - name: test_group2
    description: valid sms senders group
    receivers:
      - 37256000010
      - 37256000011
      - 37256000012
```
> PS! All groups use global `SMS_SENDER` number.

## Running app

```
$ flask run
 * Serving Flask app 'webserver'
 * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
```

## Running tests

```
$ python -m pytest -v --cache-clear

========= test session starts =========
collected 18 items

tests/functional/test_get_health.py::test_get_health PASSED
tests/unit/app/test_config.py::test_config_loaded PASSED
tests/unit/app/test_factory.py::test_app_created_with_test_config PASSED
tests/unit/app/test_log_filters.py::test_filter_remove_date_from_werkzeug_logs PASSED
tests/unit/app/test_log_filters.py::test_filter_exclude_head_logs_filtered PASSED
tests/unit/app/test_log_filters.py::test_filter_exclude_head_logs_allows_other_requests PASSED
tests/unit/telia_validations/test_receivers.py::test_validate_no_receivers_provided_not_empty PASSED
tests/unit/telia_validations/test_receivers.py::test_validate_no_receivers_provided_empty PASSED
tests/unit/telia_validations/test_receivers.py::test_validate_max_receivers_not_reached PASSED
tests/unit/telia_validations/test_receivers.py::test_validate_max_receivers_limit_reached PASSED
tests/unit/telia_validations/test_receivers.py::test_validate_receiver_whitelisted PASSED
tests/unit/telia_validations/test_receivers.py::test_validate_receiver_not_whitelisted PASSED
tests/unit/telia_validations/test_sms.py::test_validate_is_sms_messages_list_not_empty PASSED
tests/unit/telia_validations/test_sms.py::test_validate_is_sms_messages_list_empty PASSED
tests/unit/telia_validations/test_sms.py::test_validate_sms_text_has_content PASSED
tests/unit/telia_validations/test_sms.py::test_validate_sms_text_no_content PASSED 

========= 16 passed in 0.12s ===========
```
> PS. For running only specific tests: `python -m pytest -v --cache-clear -k auth`

## Tests coverage report

```
$ python -m pytest -v --cov --cov-report=term-missing --cov-report=html:htmlcov --cov-report=xml

Name                                        Stmts   Miss  Cover   Missing
-------------------------------------------------------------------------
app.py                                         27      0   100%
application/api/get_health.py                  12      0   100%
application/api/post_sms.py                    18      4    78%   50-60
application/api/post_sms_alertmanager.py       23      4    83%   61-71
application/services/telia_rest_api.py         52     32    38%   48-60, 63, 66-82, 85-88, 99-126
application/services/telia_validations.py      37      0   100%
config.py                                      28      0   100%
log_filters.py                                 10      0   100%
-------------------------------------------------------------------------
TOTAL                                         207     40    81%

Coverage HTML written to dir htmlcov
```
> PS. `Missing: 61-71` means exact line numbers not hit by tests.

## Sonarqube code analysis

Using [sonar-scanner-cli](https://docs.sonarsource.com/sonarqube-server/latest/analyzing-source-code/scanners/sonarscanner/)
```
cd ./src
sonar-scanner \
  -Dsonar.host.url=${SONAR_HOST_URL} \
  -Dsonar.token=${SONAR_TOKEN} \
  -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
  -Dsonar.projectName=${SONAR_PROJECT_NAME}
```
NB! Run coverage first to create needed `src/coverage.xml`