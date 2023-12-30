from app.models.agent import Agent
from app.models.chat import Chat
from app.openai_client import OpenAIClient


class DemoWeatherAgent3(Agent):
    """
    A weather agent that uses an API to get weather information.
    """
    def __init__(self):
        super().__init__(
            agent_id='demo_weather_agent_3',
            name='WEATHER IN JÖNKÖPING',
            short_description='Fetch weather data for JÖNKÖPING',
            forward_last_memory_to_parent=True,
        )

    def select_action(self, openai_client: OpenAIClient, action_map: dict, chat: Chat = None, memories=None):
        return 0

