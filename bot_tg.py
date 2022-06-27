import logging
import os
import telegram

from dotenv import load_dotenv
from google.api_core.exceptions import GoogleAPIError
from telegram.ext import Updater, MessageHandler, Filters

from google_dialogflow_api import detect_intent_text
from telegram_logger import TelegramLogsHandler

logger = logging.getLogger("tg_bot_logger")


def answer_text(update, context):
    dialogflow_project_id = os.getenv("GOOGLE_DIALOGFLOW_PROJECT_ID")
    session_id = update.message.from_user.id
    intent_text = update.message.text

    try:
        is_fallback, fulfillment_text = detect_intent_text(project_id=dialogflow_project_id, session_id=session_id,
                                                           text=intent_text, language_code='ru-RU')
    except GoogleAPIError as err:
        logger.exception(f'GoogleAPIError: {err}')
    else:
        try:
            update.message.reply_text(fulfillment_text)
        except telegram.error.TelegramError as err:
            logger.exception(f'TelegramError: {err}')


def main():
    load_dotenv()

    telegram_token = os.getenv("TELEGRAM_TOKEN")
    telegram_recipient_chat_id = os.getenv("TELEGRAM_RECIPIENT_CHAT_ID")

    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(telegram_token, int(telegram_recipient_chat_id)))
    logger.info('Bot TG is started')

    updater = Updater(telegram_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, answer_text))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
