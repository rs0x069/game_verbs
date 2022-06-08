import logging
import os
import telegram

from dotenv import load_dotenv
from google.api_core.exceptions import GoogleAPIError
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logger = logging.getLogger("tg_bot_logger")


class TelegramLogsHandler(logging.Handler):
    def __init__(self, token: str, chat_id: int):
        super().__init__()
        self.token = token
        self.chat_id = chat_id

        self.bot = telegram.Bot(token=self.token)

    def emit(self, record):
        log_entry = self.format(record)
        try:
            self.bot.send_message(self.chat_id, log_entry)
        except telegram.error.TelegramError as err:
            logging.exception(err)


def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    from google.cloud import dialogflow

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    for text in texts:
        text_input = dialogflow.TextInput(text=text, language_code=language_code)

        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        print("=" * 20)
        print("Query text: {}".format(response.query_result.query_text))
        print(
            "Detected intent: {} (confidence: {})\n".format(
                response.query_result.intent.display_name,
                response.query_result.intent_detection_confidence,
            )
        )

        fulfillment_text = response.query_result.fulfillment_text

        print("Fulfillment text: {}\n".format(fulfillment_text))

        return fulfillment_text


def start_command(update, context):
    update.message.reply_text('Здравствуйте!')


def help_command(update, context):
    update.message.reply_text('Help!')


def echo_message(update, context):
    update.message.reply_text(update.message.text)


def answer_text(update, context):
    dialogflow_project_id = os.getenv("GOOGLE_DIALOGFLOW_PROJECT_ID")
    intent_text = [update.message.text]
    try:
        fulfillment_text = detect_intent_texts(project_id=dialogflow_project_id, session_id='197598472',
                                               texts=intent_text, language_code='ru-RU')
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
    logger.info('Bot is started')

    updater = Updater(telegram_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start_command))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, answer_text))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
