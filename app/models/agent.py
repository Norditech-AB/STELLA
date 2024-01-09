import os

from dotenv import load_dotenv

from app.models.chat import Chat
from app.openai_client import OpenAIClient
from app.utils.request_builder import RequestBuilder
# Load the environment variables from the .env file
load_dotenv()


class Agent:
    """
    Loads and stores information about an agent
    """
    default_system_action_selection_instructions = "\n\n==== INSTRUCTIONS ====\n" \
                                                   "Carefully examine the chat history. " \
                                                   "Focus on the user's latest request and " \
                                                   "select the most relevant action to help solve the user's request." \
                                                   "Only output the index of the action you want to use. Do not " \
                                                   "output any other text except the number. " \
                                                   "\n\nCarefully analyze the provided details from your previous " \
                                                   "actions. If there is enough information to " \
                                                   "answer the user's request, or if no available actions are" \
                                                   " relevant to help solve the user's request, respond with '0'. "
    default_system_response_instructions = "\n\n==== INSTRUCTIONS ====\n" \
                                           "Generate an appropriate response to the user's request using the " \
                                           "provided details. Focus on the user's latest message, and use the " \
                                           "provided details to respond in a proper manner. Don't lie or make " \
                                           "things up. Be as helpful, nice and concise as possible."
    default_done_condition = "If the user's task has been completed and you want to generate a response"

    def __init__(
            self,
            agent_id: str,
            name: str,
            short_description: str,
            model_for_action_selection: str = 'gpt-4-1106-preview',  # GPT-4 Turbo
            model_for_response: str = 'gpt-4-1106-preview',  # GPT-4 Turbo
            wants_chat: bool = True,
            wants_memories: bool = True,
            forward_all_memory_entries_to_parent: bool = False,
            forward_last_memory_to_parent: bool = False,
            system_action_selection_instructions: str = default_system_action_selection_instructions,
            system_response_instructions: str = default_system_response_instructions,
            done_condition: str = default_done_condition,
            skip_response: bool = False,
            skip_action_selection: bool = False,
            connections_forced: dict = None,
            connections_available: dict = None,
            max_depth: int = None,
            on_completion: callable = None,
    ):
        self.agent_id = agent_id
        self.name = name
        self.short_description = short_description
        self.model_for_action_selection = model_for_action_selection
        self.model_for_response = model_for_response
        self.wants_chat = wants_chat
        self.wants_memories = wants_memories
        self.forward_all_memory_entries_to_parent = forward_all_memory_entries_to_parent
        self.forward_last_memory_to_parent = forward_last_memory_to_parent
        self.system_action_selection_instructions = system_action_selection_instructions
        self.system_response_instructions = system_response_instructions
        self.done_condition = done_condition
        self.skip_response = skip_response
        self.skip_action_selection = skip_action_selection
        self.connections_forced = connections_forced
        self.connections_available = connections_available
        self.max_depth = max_depth if max_depth is not None else int(os.getenv('AGENT_MAX_DEPTH', 99999999))
        self.on_completion = on_completion

        if self.connections_forced is None:
            self.connections_forced = {}
        if self.connections_available is None:
            self.connections_available = {}

    @staticmethod
    def _construct_memory_string(memories):
        if not memories:
            return ""
        memory_string = "=== AVAILABLE INFORMATION ===\n"
        for memory in memories:
            memory_string += f"{memory}"
        memory_string += "\n"
        return memory_string

    @staticmethod
    def _construct_chat_string(chat: Chat):
        chat_string = "=== CHAT WITH THE USER ===\n"
        for message in chat.chat_history:
            role = message['role']
            message = message['content']
            chat_string += f"{role}: {message}\n"
        chat_string += "=== (END OF CHAT) ===\n\n"
        return chat_string

    def _construct_available_actions_string(self, action_map: dict):
        available_actions_string = "=== AVAILABLE ACTIONS ===\n"
        available_actions_string += f"0: Done - Respond to the user ({self.done_condition})\n"
        for action_id in action_map.keys():
            available_actions_string += f"{action_id}: {action_map[action_id].short_description}\n"
        available_actions_string += "=== (END OF AVAILABLE ACTIONS) ===\n"
        return available_actions_string

    def select_action(self, openai_client: OpenAIClient, action_map: dict, chat: Chat = None, memories=None):
        """
        Uses the Action Map to select an action
        :param openai_client:
        :param action_map:
        :param chat:
        :param memories:
        :return:
        """
        system_message = self.system_action_selection_instructions

        user_message = f"{self._construct_memory_string(memories) if memories else ''}" \
                       f"{self._construct_chat_string(chat) if chat else ''}" \
                       f"{self._construct_available_actions_string(action_map)}" \
                       f"{self.system_action_selection_instructions}"

        messages = [
            {
                "role": "system",
                "content": system_message
            },
            {
                "role": "user",
                "content": user_message
            }
        ]

        action_selected = openai_client.chat_completion(
            messages=messages,
            model=self.model_for_action_selection,
        )

        return action_selected


    def respond(self, openai_client: OpenAIClient, request_builder: RequestBuilder, chat: Chat = None, memories=None):
        system_message = self.system_response_instructions

        user_message = f"{self._construct_memory_string(memories) if memories else ''}" \
                       f"{self._construct_chat_string(chat) if chat else ''}" \
                       f"{self.system_response_instructions}"

        messages = [
            {
                "role": "system",
                "content": system_message
            },
            {
                "role": "user",
                "content": user_message
            }
        ]

        response_generated = openai_client.chat_completion(
            messages=messages,
            model=self.model_for_response,
        )

        return response_generated
