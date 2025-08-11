import pytest
from application.core.alert_payload import AlertmanagerPayload
from application.schemas.api.api_post_body import AlertmanagerWebhookPayload

@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("test_group1,test_group2", ["test_group1", "test_group2"]),
        ("test_group1,    test_group2", ["test_group1", "test_group2"]),
        ("test_group1   ,  ,   test_group2", ["test_group1", "test_group2"]),
        ("test_group1,", ["test_group1"]),
        (",test_group1,", ["test_group1"]),
    ],
    ids=[
        "simple_comma_separated",
        "comma_with_spaces",
        "extra_commas_and_spaces",
        "trailing_comma",
        "leading_and_trailing_comma",
    ]
)
def test_url_param_string_to_list(input_str, expected, app):
    with app.app_context():
        payload = AlertmanagerPayload()
        result = payload.receivers_string_to_list(input_str)
        assert result == expected

@pytest.mark.parametrize(
    "json_path, expected_result",
    [
        ('tests/mock_data/post-alertmanager_success_1groups/api-endpoint_request.json', 'severity: critical summary: CPU usage is above 90% '),
    ],
    ids=[
        "example-alert1",
    ]
)
def test_parse_alertmanager_body_to_smstext(app, load_mock_json, json_path, expected_result):
    mock_data = load_mock_json(json_path)
    alert = AlertmanagerPayload()
    
    with app.app_context():
        alert_payload = AlertmanagerWebhookPayload(**mock_data)

        result = alert.parse_alert_to_smstext(alert_payload)

        assert result == expected_result