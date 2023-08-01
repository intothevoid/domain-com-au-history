import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from app_config import APP_CONFIG
from util import generate_hash, generate_sleep_seconds, cleanup, remove_element
from pdf import generate_pdf


def get_property_history_screenshots(property_address: str) -> dict:
    # cleanup the images and pdfs folder
    cleanup()

    chrome_options = Options()
    chrome_options.binary_location = (
        APP_CONFIG["chrome_path"] or "/opt/google/chrome/chrome"
    )

    # Local testing - uncomment if running locally on Mac
    # chrome_options.binary_location = (
    #     r"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    # )

    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(options=chrome_options)

    # open the domain.com.au property profile page
    driver.get(APP_CONFIG["domain_profile_url"])
    time.sleep(generate_sleep_seconds(3, 5))

    # search for the property address
    search_box = driver.find_element(By.CSS_SELECTOR, 'input[type="search"]')
    search_box.send_keys(property_address)
    time.sleep(generate_sleep_seconds(3, 5))

    # click on the first result
    search_box.send_keys(Keys.ENTER)
    time.sleep(generate_sleep_seconds(1, 3))

    # remove popup
    for popup in APP_CONFIG["popups"]:
        remove_element(driver, popup)

    # create list of images to be captured
    screenshot_list = []
    img_idx = 0

    # property hash
    prop_hash = generate_hash(property_address)

    # property screenshot
    prop_image = APP_CONFIG["prop_image"]
    prop_image_el = driver.find_element(By.CSS_SELECTOR, prop_image)
    prop_image_file = f"images/{prop_hash}_{img_idx}.png"
    prop_image_el.screenshot(prop_image_file)
    screenshot_list.append(prop_image_file)
    img_idx += 1

    for image_div in APP_CONFIG["image_divs"]:
        div_element = driver.find_element(By.CSS_SELECTOR, image_div)

        # Capture the screenshot of the div element containing the price history
        screenshot_file = f"images/{prop_hash}_{img_idx}.png"  # Specify the file name to save the screenshot
        div_element.screenshot(screenshot_file)
        screenshot_list.append(screenshot_file)
        img_idx += 1
        time.sleep(1)

    # get current url
    current_url = driver.current_url

    # quit the driver
    driver.quit()

    return {
        "address": property_address,
        "screenshots": screenshot_list,
        "url": current_url,
    }


def generate_property_pdf_report(info: dict) -> str:
    """generates a pdf report for the property"""
    address = info["address"]
    url = info["url"]
    image_names = info["screenshots"]
    requestor = info["requestor"]

    pdf_file = generate_pdf(address, url, image_names, requestor)

    return pdf_file


if __name__ == "__main__":
    result = get_property_history_screenshots("2 bridgeford ave, blacktown, nsw 2148")
    pdf_path = generate_property_pdf_report(result)
