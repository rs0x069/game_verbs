import logging
import os
import random

import vk_api as vk

from dotenv import load_dotenv
from google.api_core.exceptions import GoogleAPIError
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.exceptions import VkApiError

from google_dialogflow_api import detect_intent_text
from telegram_logger import TelegramLogsHandler

logger = logging.getLogger("vk_bot_logger")


def answer_text(event, vk_api, session_id):
    dialogflow_project_id = os.getenv("GOOGLE_DIALOGFLOW_PROJECT_ID")
    intent_text = event.text

    is_fallback, fulfillment_text = detect_intent_text(
        project_id=dialogflow_project_id,
        session_id=session_id,
        text=intent_text,
        language_code='ru-RU'
    )
    if not is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=fulfillment_text,
            random_id=random.randint(1, 1000)
        )


def main():
    load_dotenv()

    telegram_token = os.getenv("TELEGRAM_TOKEN")
    telegram_recipient_chat_id = os.getenv("TELEGRAM_RECIPIENT_CHAT_ID")

    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(telegram_token, int(telegram_recipient_chat_id)))
    logger.info('Bot VK is started')

    vk_token = os.getenv("VK_TOKEN")
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            session_id = 'vk-' + str(event.user_id)
            try:
                answer_text(event, vk_api, session_id)
            except GoogleAPIError as err:
                logger.exception(f'GoogleAPIError: {err}')
            except VkApiError as err:
                logger.exception(f'VkApiError: {err}')


if __name__ == '__main__':
    main()
