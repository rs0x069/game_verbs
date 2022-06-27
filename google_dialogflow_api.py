from google.cloud import dialogflow


def detect_intent_text(project_id, session_id, text, language_code):
    """Returns the result of detect intent with text as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    is_fallback = response.query_result.intent.is_fallback
    fulfillment_text = response.query_result.fulfillment_text

    return is_fallback, fulfillment_text
