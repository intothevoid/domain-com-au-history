import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def get_property_history_screenshot():
    chrome_options = Options()
    chrome_options.binary_location = r"/opt/google/chrome/chrome"
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)

    driver.get('https://www.domain.com.au/property-profile')
    time.sleep(5)

    search_box = driver.find_element(By.CSS_SELECTOR, 'input[type="search"]')
    search_box.send_keys('6 Lecornu Street, Broadview, SA 5083')
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
    get_property_history_screenshot()
    print('done creating screenshot')
    time.sleep(300)
    print('exiting...')

