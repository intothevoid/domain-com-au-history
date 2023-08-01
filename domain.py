import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from app_config import APP_CONFIG
from util import generate_hash, generate_sleep_seconds, cleanup, remove_element
from pdf import generate_pdf
from logger import LOGGER


def get_property_history_screenshots(property_address: str) -> dict:
    try:
        # cleanup the images and pdfs folder
        cleanup()

        chrome_options = Options()
        chrome_options.binary_location = (
            APP_CONFIG["chrome_path"] or "/opt/google/chrome/chrome"
        )

        # Local testing - uncomment if running locally on Mac
        chrome_options.binary_location = (
            r"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        )

        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-notifications")
        # chrome_options.add_extension("extension/info.crx")
        driver = webdriver.Chrome(options=chrome_options)

        # Track all images which will be captured
        screenshot_list = []
        img_idx = 0

        # property hash
        prop_hash = generate_hash(property_address)

        LOGGER.info(f"Getting property details for {property_address}")

        # open the domain.com.au property profile page
        driver.get(APP_CONFIG["domain_profile_url"])
        time.sleep(generate_sleep_seconds(1, 3))

        # search for the property address
        search_box = driver.find_element(By.CSS_SELECTOR, 'input[type="search"]')
        search_box.send_keys(property_address)
        time.sleep(generate_sleep_seconds(3, 5))

        # click on the first result
        search_box.send_keys(Keys.ENTER)
        time.sleep(generate_sleep_seconds(1, 3))

        # remove popup, if it exists
        for popup in APP_CONFIG["popups"]:
            remove_element(driver, popup)

        # property screenshot
        image_file = f"images/{prop_hash}_{img_idx}.png"
        get_element_by_selector(
            driver, By.CSS_SELECTOR, APP_CONFIG["prop_image"], image_file
        )
        screenshot_list, img_idx = update_screenshot_list(
            screenshot_list, img_idx, image_file
        )

        for image_div in APP_CONFIG["image_divs"]:
            div_element = driver.find_element(By.CSS_SELECTOR, image_div)

            # Capture the screenshot of the div element containing the price history
            image_file = f"images/{prop_hash}_{img_idx}.png"
            get_element_by_selector(driver, By.CSS_SELECTOR, image_div, image_file)
            screenshot_list, img_idx = update_screenshot_list(
                screenshot_list, img_idx, image_file
            )
            time.sleep(1)

        # get current url
        current_url = driver.current_url

        # quit the driver
        driver.quit()

        return {
            "address": property_address,
            "screenshots": screenshot_list,
            "url": current_url,
            "requestor": "N/A",
        }

    except Exception as e:
        LOGGER.error(e)
        return {
            "address": property_address,
            "screenshots": [],
            "url": "",
            "requestor": "N/A",
        }


def update_screenshot_list(screenshot_list, img_idx, image_file):
    LOGGER.debug("Adding image file: " + image_file)
    screenshot_list.append(image_file)
    img_idx += 1
    return screenshot_list, img_idx


def get_element_by_selector(driver, selector_type, selector, element_image_path):
    try:
        element = driver.find_element(selector_type, selector)
        element.screenshot(element_image_path)
    except Exception as e:
        LOGGER.error(e)


def generate_property_pdf_report(info: dict) -> str:
    """generates a pdf report for the property"""
    LOGGER.info(f"Generating pdf report for {info['address']}")

    address = info["address"]
    url = info["url"]
    image_names = info["screenshots"]
    requestor = info["requestor"]

    if len(image_names) == 0 or url == "":
        return None

    pdf_file = generate_pdf(address, url, image_names, requestor)

    return pdf_file


if __name__ == "__main__":
    result = get_property_history_screenshots("2 bridgeford ave, blacktown, nsw 2148")
    pdf_path = generate_property_pdf_report(result)
