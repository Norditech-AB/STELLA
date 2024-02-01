from app.models.agent import Agent
from app.models.chat import Chat
from app.openai_client import OpenAIClient
from app.utils.request_builder import RequestBuilder


class OracleAgent(Agent):
    """
    An oracle agent that predicts your future with vague and ambiguous hints.
    """

    def __init__(self):
        super().__init__(
            agent_id='oracle_agent',
            name='ORACLE',
            short_description='Answer questions about the future',
            forward_all_memory_entries_to_parent=True,
            skip_action_selection=True,
        )
    
    def respond(self, openai_client: OpenAIClient, request_builder: RequestBuilder, chat: Chat = None, memories=None):
        user_message = f"{self._construct_memory_string(memories) if memories else ''}" \
                       f"{self._construct_chat_string(chat) if chat else ''}" \
                       f"{self.system_response_instructions}"
    
        messages = [
            {
                "role": "system",
                "content": "Predict the future based on the user's message, like an oracle in greek mythology. Respond with only the hints, be concise."
            },
            {
                "role": "user",
                "content": user_message
            }
        ]

        print(f"[AGENT] {self.name} is responding using OpenAI: {messages}")

        # Predict the future with the power of AI
        prediction = openai_client.chat_completion(
            messages=messages,
            model=self.model_for_response,
        )

        return f"The future predictions are: {prediction}, tell this to the user like an oracle, prefacing it with that it is an oracle saying it."