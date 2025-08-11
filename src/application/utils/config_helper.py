
import yaml
from application.schemas.config.sms_receivers_yaml import SMSReceiversConfig

def load_yaml_config(yaml_config_path : str):
    with open(yaml_config_path, "r") as f:
        yaml_config = yaml.safe_load(f) or {}
        yaml_config = SMSReceiversConfig(**yaml_config) # unpack dict
        return yaml_config