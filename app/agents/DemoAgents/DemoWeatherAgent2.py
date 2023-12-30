from app.models.agent import Agent
from app.models.chat import Chat
from app.openai_client import OpenAIClient


class DemoWeatherAgent2(Agent):
    """
    A weather agent that uses an API to get weather information.
    """
    def __init__(self):
        super().__init__(
            agent_id='demo_weather_agent_2',
            name='WEATHER IN STOCKHOLM',
            short_description='Fetch weather data for STOCKHOLM',
            forward_last_memory_to_parent=True,
            skip_action_selection=True,
        )

    def respond(self, openai_client: OpenAIClient, request_builder, chat: Chat = None, memories=None):
        return "The weather in Stockholm is +19 degrees Celsius, with a 25% chance of rain. Sun is out."




