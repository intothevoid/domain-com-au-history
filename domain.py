import os
import logging
import random
import time
import yaml
import apprise
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def setup_logger():
    # create logger
    logger = logging.getLogger('domain')
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    return logger

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
LOGGER = setup_logger()
TELEGRAM_TOKEN = get_env_var("PROP_TELEGRAM_BOT") or APP_CONFIG["telegram_token"] or ""

# function which generates a hash from a string
# security is not a concern here, just want to avoid sending duplicate messages
def generate_hash(string: str):
    return hash(string)

# function which generates a random value between min and max
def generate_random_value(min: int, max: int):
    return random.randint(min, max)



def setup_telegram_bot():
    # use apprise to send telegram message
    apobj = apprise.Apprise()
    apobj.add('tgram://bot_token/chat_id')
    return apobj

def get_property_history_screenshot(property_address: str):
    chrome_options = Options()
    chrome_options.binary_location = APP_CONFIG['chrome_path'] or "/opt/google/chrome/chrome"
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(APP_CONFIG['domain_profile_url'])
    time.sleep(generate_random_value(3,5))

    # search for the property address
    search_box = driver.find_element(By.CSS_SELECTOR, 'input[type="search"]')
    search_box.send_keys(property_address)
    time.sleep(generate_random_value(3,5))

    # click on the first result
    search_box.send_keys(Keys.ENTER)
    time.sleep(generate_random_value(1,3))

    # grab a screenshot of the price history
    # Locate the div element using its class name
    div_element = driver.find_element(By.CLASS_NAME, 'css-ubxrdl')

    # Capture the screenshot of the div element containing the price history
    screenshot_file = f'images/{generate_hash(property_address)}.png'  # Specify the file name to save the screenshot
    div_element.screenshot(screenshot_file)
    time.sleep(generate_random_value(3,5))
    
    # quit the driver
    driver.quit()

if __name__ == '__main__':
    LOGGER.info('starting domain.com.au property history bot...')

    get_property_history_screenshot('18 Janet Street, Merewether NSW 2291')
    print('done creating screenshot')

    # while loop to check for new properties
    while True:
        # telegram bot loop waiting for new messages
        # if new message, check if it is a property address
        # if property address, check if it is in the database
        # if not in database, add to database and send message
        # if in database, check if price has changed
        # if price has changed, send message
        # if price has not changed, do nothing
        time.sleep(5)
        print('waiting for new messages...')

