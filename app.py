from telegram_bot import start_telegram_bot
from logger import LOGGER
from app_config import TELEGRAM_TOKEN

if __name__ == '__main__':
    LOGGER.info('starting domain.com.au property history bot...')

    # call the telegram bot
    start_telegram_bot(TELEGRAM_TOKEN)