from app.models.agent import Agent
from app.models.chat import Chat
from app.openai_client import OpenAIClient


class DemoWeatherAgent(Agent):
    """
    A weather agent that uses an API to get weather information.
    """
    def __init__(self):
        super().__init__(
            agent_id='demo_calendar_agent',
            name='CALENDAR',
            short_description='View calendar events',
            forward_last_memory_to_parent=True,
            skip_action_selection=True,
        )

    def respond(self, openai_client: OpenAIClient, request_builder, chat: Chat = None, memories=None):
        return "=== CALENDAR ===\n" \
               "6 Nov 13:00 CET - 14:00 CET: Meeting with Johan\n" \
               "6 Nov 14:30 CET - 15:30 CET: Lunch with Maria\n" \
               "7 Nov 10:00 CET - 11:00 CET: Meeting with Johan\n==="
