import random
import hashlib

from selenium.webdriver.common.by import By

from logger import LOGGER

# function which generates a hash from a string
# security is not a concern here, just want to avoid sending duplicate messages
def generate_hash(string: str):
    return hashlib.md5(b"{string}").hexdigest()[:10]

# function which generates a random value between min and max
def generate_sleep_seconds(min: int, max: int):
    random_val = random.randint(min, max)
    LOGGER.info(f'sleeping for {random_val} seconds...')
    return random_val

# function to clean up the images and pdfs folder
def cleanup():
    import os
    import glob

    # remove all files in images folder
    files = glob.glob('images/*')
    for f in files:
        os.remove(f)

    # remove all files in pdfs folder
    files = glob.glob('pdfs/*')
    for f in files:
        os.remove(f)

def remove_element(driver, selector: str):
    """removes an element from the page
    """
    element = driver.find_element(By.CSS_SELECTOR, selector)
    driver.execute_script("""
        var element = arguments[0];
        element.parentNode.removeChild(element);
        """, element)