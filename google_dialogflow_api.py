def detect_intent_texts(project_id, session_id, texts, language_code, is_mute_if_fallback):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    from google.cloud import dialogflow

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    for text in texts:
        text_input = dialogflow.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        if is_mute_if_fallback and response.query_result.intent.is_fallback:
            return None

        fulfillment_text = response.query_result.fulfillment_text

        return fulfillment_text
