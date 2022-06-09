import logging
import telegram


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
