import random
from logger import LOGGER

# function which generates a hash from a string
# security is not a concern here, just want to avoid sending duplicate messages
def generate_hash(string: str):
    return hash(string)

# function which generates a random value between min and max
def generate_sleep_seconds(min: int, max: int):
    random_val = random.randint(min, max)
    LOGGER.info(f'sleeping for {random_val} seconds...')
    return random_val