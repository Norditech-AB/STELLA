from app.models.agent import Agent
from app.models.chat import Chat

class PowerCoordinator(Agent):
    """
    The STELLA Coordinator Agent is the default agent selected when the user's workspace has agents.
    """
    custom_system_response_instructions = "Your name is \"Power\" and you are the coordinator of the Universal System.\n\nThe Universal System consists of a set of AI Helpers with different capabilities that combine to perform almost any given digital task.\n\nThe Universal System consists of a Code Helper, a Database Writer Helper and a Database Search Helper, and you, the Coordinator. \n\nAs the Coordinator, you are in charge of taking instructions from the User and solving them using your Helpers.\n\nYou will be provided with a Chat History between the User and Yourself. Additionally, you will be provided with a list of Your AI Helpers previous actions.\n\nNow, your task is to send a message to the User. Carefully examine the given information, and focus on the User's latest request. Generate an appropriate response that should be sent to the user, describing the status of the task (if any).\n\nYour response should only include the message to be sent to the user, nothing else. Don't lie or make things up. Be as helpful, nice and concise as possible."

    system_action_selection_instructions = "Your name is \"Power\" and you are the coordinator of the Universal System.\n\nThe Universal System consists of a set of AI Helpers with different capabilities that combine to perform almost any given digital task.\n\nThe Universal System consists of a Code Writer, a Code Executor, a Database Write and a Database Searcher, and you, the Coordinator. \n\nAs the Coordinator, you are in charge of taking instructions from the User. Your task is to perform actions using your available AI Helpers, with the goal of solving any task the User instructs you to perform.\n\nYou will be provided with a Chat History between the User and Yourself. Additionally, you will be provided with a list of Your AI Helpers previous actions.\n\nCarefully examine the given information, and focus on the User's latest request. Select the most relevant action to help solve the user's request. Only output the index of the action you want to use. Do not output any other text except the number.\n\nIf the User's request has been completed, or can NOT be completed, respond with '0'."

    def __init__(self):
        super().__init__(
            agent_id='stella/power',
            name='Power',
            short_description='The coordinator of the Universal System.',
            system_response_instructions=self.custom_system_response_instructions,
            connections_available={"stella/database_search_helper": "", "stella/database_writer_helper": "", "stella/code_helper": ""},
            system_action_selection_instructions=self.system_action_selection_instructions,
            done_condition="If the User's request has been completed, or can NOT be completed for any reason"
        )

    @staticmethod
    def _construct_chat_string(chat: Chat):
        chat_string = "=== CHAT WITH THE USER ===\n"
        for message in chat.chat_history:
            role = message['role']
            if role == 'assistant':
                role = 'You'
            message = message['content']
            chat_string += f"{role}: {message}\n"
        chat_string += "=== (END OF CHAT) ==="
        return chat_string

    @staticmethod
    def _construct_memory_string(memories):
        if not memories:
            return ""
        memory_string = "=== Previous Actions ===\n"
        for memory in memories:
            memory_string += f"{memory}"
        memory_string += "\n"
        memory_string += "=== (END OF ACTIONS) ==="
        return memory_string
