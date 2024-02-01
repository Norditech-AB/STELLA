import pytz

from app.models.agent import Agent
from app.models.chat import Chat
from app.openai_client import OpenAIClient
from app.utils.request_builder import RequestBuilder
from datetime import datetime


class DateTimeAgent(Agent):
    """
    A datetime agent that uses an API to get the current date and time around the world.
    """

    def __init__(self):
        super().__init__(
            agent_id='datetime_agent',
            name='DATETIME',
            short_description='Fetch date and time geographically',
            forward_all_memory_entries_to_parent=True,
            skip_action_selection=True,
        )
    
    @staticmethod
    def get_location_datetime(location: str) -> str:
        timezone = pytz.timezone(location)

        return datetime.now(timezone)

    def respond(self, openai_client: OpenAIClient, request_builder: RequestBuilder, chat: Chat = None, memories=None):
        user_message = f"{self._construct_memory_string(memories) if memories else ''}" \
                       f"{self._construct_chat_string(chat) if chat else ''}" \
                       f"{self.system_response_instructions}"
        
        messages = [
            {
                "role": "system",
                "content": "Extract the name of the city or country from the user's message. Only respond with the most relevant 'pytz' timezone string for that location."
            },
            {
                "role": "user",
                "content": user_message
            }
        ]

        print(f"[AGENT] {self.name} is responding using OpenAI: {messages}")

        # Extract location
        location = openai_client.chat_completion(
            messages=messages,
            model=self.model_for_response,
        )
        location = location.strip(" ").strip("'")     

        # Fetch and format datetime
        datetime = DateTimeAgent.get_location_datetime(location).strftime("%Y-%m-%d %H:%M:%S")

        # Respond with including datetime and location
        return f"Tell the user, the date and time based on the current datetime: {datetime}, for the location: {location}."
 