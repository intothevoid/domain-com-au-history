import os
from logger import LOGGER
import yaml

# function to read config.yml file
def read_config():
    with open('config.yml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config

def get_env_var(var: str):
    """Get environment variable."""
    try:
        return os.environ[var]
    except KeyError:
        LOGGER.error(f"Environment variable {var} not set")
        return None

APP_CONFIG = read_config()

# get the telegram token from the environment variable or config.yml
TELEGRAM_TOKEN = get_env_var("PROP_TELEGRAM_BOT") or APP_CONFIG["telegram_token"] or ""