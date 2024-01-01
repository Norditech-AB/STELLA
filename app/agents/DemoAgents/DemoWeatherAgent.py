from app.models.agent import Agent
from app.models.chat import Chat
from app.openai_client import OpenAIClient


class DemoWeatherAgent(Agent):
    """
    A weather agent that uses an API to get weather information.
    """
    def __init__(self):
        super().__init__(
            agent_id='demo_weather_agent',
            name='WEATHER',
            short_description='Fetch weather data',
            forward_all_memory_entries_to_parent=True,
            skip_response=True,
            connections_available={"demo_weather_agent_2": {}, "demo_weather_agent_3": {}},
            model_for_response="llama-2",
            model_for_action_selection="gpt-4"
        )
