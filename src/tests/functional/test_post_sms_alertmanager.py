import pytest
from unittest.mock import patch

@pytest.mark.parametrize(
  "url_params, request_json, telia_json, expected_response_json, telia_status_code, endpoint_status_code",
  [
    (
      '?receiver_groups=test_group2',
      'tests/mock_data/post-alertmanager_success_1groups/api-endpoint_request.json', 
      'tests/mock_data/post-alertmanager_success_1groups/telia-api_response.json',
      'tests/mock_data/post-alertmanager_success_1groups/api-endpoint_response.json',
      200,
      200
    ),
    (
      '?receiver_groups=test_group1,test_group2',
      'tests/mock_data/post-alertmanager_success_2groups/api-endpoint_request.json', 
      'tests/mock_data/post-alertmanager_success_2groups/telia-api_response.json',
      'tests/mock_data/post-alertmanager_success_2groups/api-endpoint_response.json',
      200,
      200
    )
  ],
  ids=[
    "success_request_1groups",
    "success_request_2groups"
  ]
)
@patch("application.services.telia_api.TeliaMultiSmsAPI._post_request")
def test_post_sms(
    mock_post_sms, 
    load_mock_json, 
    dict_to_response, 
    client, 
    default_auth_header, 
    url_params,
    request_json, 
    telia_json, 
    expected_response_json,
    telia_status_code,
    endpoint_status_code
  ):
  api_request = load_mock_json(request_json)
  telia_response = load_mock_json(telia_json)
  expected_api_response = load_mock_json(expected_response_json)

  # override telia-api response with mock data
  mock_post_sms.return_value = dict_to_response(telia_response, status_code=endpoint_status_code)
  mock_post_sms.status_code = telia_status_code

  response = client.post("/api/v1/webhooks/alertmanager" + url_params, json=api_request, headers=default_auth_header)

  # Remove the 'id' field if it exists in both
  response_data = response.json
  response_data.pop("id", None)
  expected_api_response.pop("id", None)

  assert response.status_code == endpoint_status_code
  assert response_data == expected_api_response