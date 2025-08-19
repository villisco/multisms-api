from flask import current_app as app
from typeguard import typechecked

from application.schemas.api.api_post_body import AlertmanagerWebhookPayload

class AlertmanagerPayload():
  @typechecked
  def receivers_string_to_list(self, receivers_str: str) -> list:
    """
    Convert URL param string into workable list.
    Example: "group1,group2,group3" ---> ["group1", "group2", "group3"]
    """
    app.logger.debug("Converting receivers_str into list: %s" % receivers_str)
    sms_groups = [item.strip() for item in receivers_str.split(",") if item.strip()]
    return sms_groups

  @typechecked
  def _merge_dict_to_string(self, parsed_alert_dict: dict) -> str:
    sms_text = ""
    for key, value in parsed_alert_dict.items():
        if value:
          sms_text += "%s: %s; " % (key, value)
    
    return sms_text

  @typechecked
  def parse_alert_to_smstext(self, alert: AlertmanagerWebhookPayload) -> str:
    app.logger.debug("Converting alert into SMS text: %s" % alert)

    parsed_alert_dict = {}

    # fields from alert we want to show in SMS text
    parsed_alert_dict["service"] = alert.alerts[0].labels.service or ""
    parsed_alert_dict["severity"] = alert.alerts[0].labels.severity or ""
    parsed_alert_dict["summary"] = alert.alerts[0].labels.summary or ""
    
    # fallbacks
    if not parsed_alert_dict["service"]:
      parsed_alert_dict["teenus"] = alert.alerts[0].labels.teenus or ""

    if not parsed_alert_dict["summary"]:
      parsed_alert_dict["summary"] = alert.alerts[0].annotations.summary or ""
    
    if not parsed_alert_dict["summary"]:
      parsed_alert_dict["summary"] = alert.alerts[0].annotations.description or ""

    sms_text = self._merge_dict_to_string(parsed_alert_dict)

    return sms_text 