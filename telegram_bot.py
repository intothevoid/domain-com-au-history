#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position

"""
Simple Telegram Bot to get the price history of an Aussie property from domain.com.au
"""

import os
from telegram import __version__ as TG_VER
from logger import LOGGER
from domain import get_property_history_screenshots, generate_property_pdf_report

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! Try /help",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        "Hi! I am a bot which can get you the property report of Aussie properties."
    )
    await update.message.reply_text(
        "Just type in the address and I will send you the property report (if available)."
    )


async def process_property_address(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Get the property address and send the price history screenshot."""
    try:
        await update.message.reply_text(
            "Please wait ~30 seconds while I generate a report for you. You will get a notification when ready."
        )
        result = get_property_history_screenshots(update.message.text)
        result["requestor"] = str(update.effective_user.username)
        pdf_report = generate_property_pdf_report(result)

        if not os.path.exists(pdf_report):
            raise Exception("PDF report not generated or failed to generate.")

        LOGGER.info(
            f"Sending property report for {str(update.message.text)} to {str(update.effective_user.username)}"
        )

        # send generated pdf report to user
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=open(pdf_report, "rb"),
            filename=f"{result['address']}.pdf",
            caption=f"Here is the property report for {result['address']}.",
        )
    except Exception as e:
        LOGGER.error(e)
        await update.message.reply_text(
            "Sorry, I couldn't get the price history for that address. Please try again in sometime."
        )


def start_telegram_bot(bot_token: str) -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(bot_token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, process_property_address)
    )

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    start_telegram_bot("bot_token")
