import os
import random

import vk_api as vk

from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType


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

        if response.query_result.intent.is_fallback:
            return None

        fulfillment_text = response.query_result.fulfillment_text

        print("Fulfillment text: {}\n".format(fulfillment_text))

        return fulfillment_text


def echo_message(event, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=random.randint(1, 1000)
    )


def answer_text(event, vk_api, session_id):
    dialogflow_project_id = os.getenv("GOOGLE_DIALOGFLOW_PROJECT_ID")
    intent_text = [event.text]

    fulfillment_text = detect_intent_texts(
        project_id=dialogflow_project_id,
        session_id=session_id, texts=intent_text,
        language_code='ru-RU'
    )
    if fulfillment_text:
        vk_api.messages.send(
            user_id=event.user_id,
            message=fulfillment_text,
            random_id=random.randint(1, 1000)
        )


def main():
    load_dotenv()

    vk_token = os.getenv("VK_TOKEN")
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            answer_text(event, vk_api, event.user_id)


if __name__ == '__main__':
    main()
