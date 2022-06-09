import os
import json

from dotenv import load_dotenv
from google.api_core.exceptions import GoogleAPIError


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""
    from google.cloud import dialogflow

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

    with open('questions.json') as questions_file:
        intents = json.load(questions_file)

    dialogflow_project_id = os.getenv("GOOGLE_DIALOGFLOW_PROJECT_ID")

    for intent in intents:
        intent_questions = intents[intent]['questions']
        intent_answer = [intents[intent]['answer']]
        try:
            create_intent(dialogflow_project_id, intent, intent_questions, intent_answer)
        except GoogleAPIError as err:
            print(f'GoogleAPIError: {err}')


if __name__ == '__main__':
    main()
