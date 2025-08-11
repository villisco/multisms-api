from flask import current_app as app
from typeguard import typechecked

from application.schemas.services.telia_payload import SmsMessage, SmsMessages
from application.utils.exceptions import ApiException, ApiError
from application.schemas.config.sms_receivers_yaml import ReceiverGroup

class TeliaPayload():
  @typechecked
  def _get_config_group(self, group_name: str) -> ReceiverGroup:
    for group in app.config.get("receiver_groups"):
      if group.name == group_name:
        return group

  @typechecked
  def _verify_groups_exist(self, req_groups: list) -> bool:
    """
    Check if all groups passed with request also exist in configuration (aka known groups).
    """
    config_groups = app.config.get("receiver_groups", [])
    config_group_names = [group.name for group in config_groups]

    if not config_groups or not req_groups:
      return False

    # compare if "receivers_list" all items are inside "config_group_names" list
    result = all(item in config_group_names for item in req_groups)
    return result # True/False
  
  @typechecked
  def _validate_sms_text_length(self, sms_text: str) -> bool:
    message_char_limit = 1530
    if len(sms_text) > message_char_limit:
        raise ValueError("SMS message exceeded allowed characters \"%i\" limit: \"%s\"" % (message_char_limit, sms_text))
    return True

  @typechecked
  def _merge_sms_receivers(self, sms_groups: list) -> list:
    """
    Different groups can contain same SMS receiver number.
    Prevents duplicate SMS generation.
    """
    sms_receivers = []
    for group_name in sms_groups:
      group = self._get_config_group(group_name)
      for receiver in group.receivers:
        if receiver not in sms_receivers:
          sms_receivers.append(receiver)

    app.logger.info("[_merge_sms_receivers] Total SMS receivers: %i" % len(sms_receivers))
    return sms_receivers

  @typechecked
  def _generate_sms_messages(self, sms_receivers_list: list, sms_text: str) -> SmsMessages:
    self._validate_sms_text_length(sms_text)

    sms_messages_list = SmsMessages()
    for sms_receiver in sms_receivers_list:
      sms_message = SmsMessage(
        flash = False,
        from_ = str(app.config["SMS_SENDER"]),
        message = sms_text,
        requestReport = True,
        to = str(sms_receiver)
      )

      sms_messages_list.messages.append(sms_message)
      app.logger.debug("[_generate_sms_messages] Generated SMS message: %s" % sms_message)

    app.logger.info("[_generate_sms_messages] Total SMS messages generated: %i" % len(sms_messages_list.messages))

    return sms_messages_list

  @typechecked
  def prepare_payload(self, sms_groups_list: list, sms_text: str) -> SmsMessages:
    if not self._verify_groups_exist(sms_groups_list):
        raise ApiException(ApiError.UNKNOWN_RECEIVER_GROUP, status_code=400)

    sms_receivers_list = self._merge_sms_receivers(sms_groups_list)
    sms_messages_list = self._generate_sms_messages(sms_receivers_list, sms_text)

    return sms_messages_list