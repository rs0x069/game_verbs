import argparse
import logging
import os
import json

from dotenv import load_dotenv
from google.api_core.exceptions import GoogleAPIError
from google.cloud import dialogflow

logger = logging.getLogger("Manage intents logger")


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    return response


def main():
    load_dotenv()

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s', '%Y-%m-%d %H:%M:%S')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    dialogflow_project_id = os.getenv("GOOGLE_DIALOGFLOW_PROJECT_ID")

    parser = argparse.ArgumentParser(description='Скрипт обучения нейронной сети фразами и ответами из json-файла')
    parser.add_argument('-f', '--file_name', default='questions.json',
                        help='Имя json-файла с фразами и ответами. По-умолчанию questions.json в папке скрипта.'
                        )
    args = parser.parse_args()

    intents = {}
    try:
        with open(args.file_name) as questions_file:
            intents = json.load(questions_file)
    except FileNotFoundError as err:
        logger.error(f'FileNotFoundError: {err}')

    # TODO: Сделать проверку формата json-файла, файл должен соответствовать шаблону
    for intent_name, intent_content in intents.items():
        intent_questions = intent_content['questions']
        intent_answer = intent_content['answer']
        try:
            create_intent(dialogflow_project_id, intent_name, intent_questions, intent_answer)
        except GoogleAPIError as err:
            logger.error(f'GoogleAPIError: {err}')


if __name__ == '__main__':
    main()
