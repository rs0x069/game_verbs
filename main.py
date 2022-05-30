import os

from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


def start_command(update, context):
    update.message.reply_text('Здравствуйте!')


def help_command(update, context):
    update.message.reply_text('Help!')


def echo_message(update, context):
    update.message.reply_text(update.message.text)


def main():
    load_dotenv()

    telegram_token = os.getenv("TELEGRAM_TOKEN")

    updater = Updater(telegram_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start_command))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo_message))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
