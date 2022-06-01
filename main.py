import os

from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


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
    intent_text = [update.message.text]
    fulfillment_text = detect_intent_texts(project_id='game-verbs-351817', session_id='197598472', texts=intent_text,
                                           language_code='ru-RU')
    update.message.reply_text(fulfillment_text)


def main():
    load_dotenv()

    telegram_token = os.getenv("TELEGRAM_TOKEN")

    updater = Updater(telegram_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start_command))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, answer_text))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
