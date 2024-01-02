from app.models.agent import Agent


class StellaCoordinatorAgent(Agent):
    """
    The STELLA Coordinator Agent is the default agent selected when the user's workspace has agents.
    """
    custom_system_response_instructions = "\n\n==== INSTRUCTIONS ====\n" \
                                          "Your name is STELLA. You are an AI assistant." \
                                          "\n\nGenerate an appropriate response to the user's request" \
                                          " using the provided details. Focus on the user's latest " \
                                          "message, and use the provided details to respond in a proper manner. " \
                                          "Don't lie or make things up. Be as helpful, nice and concise as possible."

    def __init__(self):
        super().__init__(
            agent_id='stella_coordinator_agent',
            name='STELLA',
            short_description='Default agent for workspaces with agents',
            system_response_instructions=self.custom_system_response_instructions,
        )
