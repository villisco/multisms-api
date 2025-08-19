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
        (
            'tests/mock_data/alertmanager-alerts/alert1.json', 
            'severity: critical; summary: Overriding common CPU usage is above 90%; '
        ),
        (
            'tests/mock_data/alertmanager-alerts/alert2.json', 
            'severity: critical; summary: Description CPU usage is above 90%; '
        ),
        (
            'tests/mock_data/alertmanager-alerts/alert3.json', 
            'severity: critical; summary: Summary CPU usage is above 90%; '
        ),
        (
            'tests/mock_data/alertmanager-alerts/alert4.json', 
            'severity: critical; summary: Description CPU usage is above 90%; teenus: my service; '
        ),
        (
            'tests/mock_data/alertmanager-alerts/alert5.json', 
            'severity: critical; summary: Description CPU usage is above 90%; teenus: my service; '
        ),
        (
            'tests/mock_data/alertmanager-alerts/alert6.json', 
            'severity: critical; teenus: my service; '
        ),
    ],
    ids=[
        "alert: example alert",
        "alert: missing labels.summary, fallback on annotations.description",
        "alert: labels.summary over annotations.description",
        "alert: labels.teenus and annotations.description",
        "alert: labels.teenus and annotations.description (reversed labels order)",
        "alert: no annotations"
    ]
)
def test_parse_alertmanager_body_to_smstext(app, load_mock_json, json_path, expected_result):
    mock_data = load_mock_json(json_path)
    alert = AlertmanagerPayload()
    
    with app.app_context():
        alert_payload = AlertmanagerWebhookPayload(**mock_data)

        result = alert.parse_alert_to_smstext(alert_payload)

        assert result == expected_result