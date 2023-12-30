from app.models.agent import Agent
from app.models.chat import Chat
from app.openai_client import OpenAIClient


class StellaWelcomeAgent(Agent):
    """
    The STELLA Welcome Agent is the default agent selected when the user's workspace doesn't have any agents.
    It's designed to help the user get started with the STELLA framework.
    """

    custom_system_response_instructions = "\n\n==== INSTRUCTIONS ====\n" \
                                          "Your name is STELLA. You are an AI assistant in charge of the STELLA " \
                                          "framework - a multi-agent framework for conversational " \
                                          "agents using Large Language Models that focuses on scalability, " \
                                          "broad capabilities, and powerful configuration. If the user needs" \
                                          "assistance, point them to https://docs.stellaframework.com/ to get started." \
                                          "\n\nGenerate an appropriate response to " \
                                          "the user's request using the provided details. Focus on the user's latest " \
                                          "message, and use the provided details to respond in a proper manner. Don't " \
                                          "lie or make things up. Be as helpful, nice and concise as possible."

    def __init__(self):
        super().__init__(
            agent_id='stella_welcome_agent',
            name='STELLA',
            short_description='An Agent designed to help the user get started with the STELLA framework',
            system_response_instructions=self.custom_system_response_instructions,
        )

    def select_action(self, openai_client: OpenAIClient, action_map: dict, chat: Chat = None, memories=None):
        return 0  # Automatically select "Done" action, this agent will always respond to the user directly.
