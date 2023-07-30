import logging
import time
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

APP_CONFIG = read_config()
LOGGER = setup_logger()

# function to read config.yml file
def read_config():
    with open('config.yml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config


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

def get_property_history_screenshot(property_address: str):
    chrome_options = Options()
    chrome_options.binary_location = APP_CONFIG['chrome_path'] or "/opt/google/chrome/chrome"
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(APP_CONFIG['domain_url'])
    time.sleep(5)

    search_box = driver.find_element(By.CSS_SELECTOR, 'input[type="search"]')
    search_box.send_keys(property_address)
    time.sleep(2)
    search_box.send_keys(Keys.ENTER)
    time.sleep(5)

    # grab a screenshot of the price history
    # Locate the div element using its class name
    div_element = driver.find_element(By.CLASS_NAME, 'css-ubxrdl')

    # Capture the screenshot of the div element
    screenshot_file = 'div_screenshot.png'  # Specify the file name to save the screenshot
    div_element.screenshot(screenshot_file)

    time.sleep(5)
    driver.quit()

if __name__ == '__main__':
    LOGGER.info('starting property helper bot...')

    get_property_history_screenshot()
    print('done creating screenshot')
    time.sleep(300)
    print('exiting...')

