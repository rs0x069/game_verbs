import json

from dotenv import load_dotenv


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

    dialogflow_project_id = 'game-verbs-351817'
    intent_name = 'Как устроиться к вам на работу'

    first_intent = list(intents.keys())[0]
    intent_questions = intents[first_intent]['questions']
    intent_answer = [intents[first_intent]['answer']]

    create_intent(dialogflow_project_id, intent_name, intent_questions, intent_answer)


if __name__ == '__main__':
    main()
