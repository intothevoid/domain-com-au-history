import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from app_config import APP_CONFIG
from util import generate_hash, generate_sleep_seconds

def get_property_history_screenshot(property_address: str):
    chrome_options = Options()
    chrome_options.binary_location = APP_CONFIG['chrome_path'] or "/opt/google/chrome/chrome"
    
    # Local testing
    # chrome_options.binary_location = r"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)

    # open the domain.com.au property profile page
    driver.get(APP_CONFIG['domain_profile_url'])
    time.sleep(generate_sleep_seconds(3,5))

    # search for the property address
    search_box = driver.find_element(By.CSS_SELECTOR, 'input[type="search"]')
    search_box.send_keys(property_address)
    time.sleep(generate_sleep_seconds(3,5))

    # click on the first result
    search_box.send_keys(Keys.ENTER)
    time.sleep(generate_sleep_seconds(1,3))

    # grab a screenshot of the price history
    # Locate the div element using its class name
    div_element = driver.find_element(By.CLASS_NAME, 'css-ubxrdl')

    # get current url
    current_url = driver.current_url

    # Capture the screenshot of the div element containing the price history
    screenshot_file = f'images/{generate_hash(property_address)}.png'  # Specify the file name to save the screenshot
    div_element.screenshot(screenshot_file)
    time.sleep(generate_sleep_seconds(3,5))
    
    # quit the driver
    driver.quit()

    return screenshot_file, current_url