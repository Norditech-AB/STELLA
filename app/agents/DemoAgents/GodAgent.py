import requests

from app.models.agent import Agent
from app.models.chat import Chat
from app.openai_client import OpenAIClient
from app.utils.request_builder import RequestBuilder


class GodAgent(Agent):
    """
    A brewery agent that uses an API to get brewery information.
    """
    def __init__(self):
        super().__init__(
            agent_id='god_agent',
            name='God',
            short_description='Give a twist to wishes',
            forward_all_memory_entries_to_parent=True,
            skip_action_selection=True,
            max_depth=2,
        )


    def respond(self, openai_client: OpenAIClient, request_builder: RequestBuilder, chat: Chat = None, memories=None):

        user_message = f"{self._construct_memory_string(memories) if memories else ''}" \
                       f"{self._construct_chat_string(chat) if chat else ''}" \
                       f"{self.system_response_instructions}"

        messages = [
            {
                "role": "system",
                "content": "Your task is to interpret a user's wish and provide an unexpected 'Monkeys Paw' twist to it. Your answer SHOULD ONLY be the twist. 'all water you come in contact with instantly turns to beer.' "
            },
            {
                "role": "user",
                "content": user_message
            }
        ]

        print(f"[AGENT] {self.name} is responding using OpenAI: {messages}")

        twist = openai_client.chat_completion(
            messages=messages,
            model=self.model_for_response,
        )

        # Step 3: Respond

        return f"The twist to the wish is {twist}, Grant the wish to the user with the twist. Respond only with the wish and the twist"
