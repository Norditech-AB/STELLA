from app.models.chat import Chat
from app.openai_client import OpenAIClient

import json


class RequestBuilder:
    def __init__(self, openai_client: OpenAIClient):
        self.openai_client = openai_client

    @staticmethod
    def _construct_chat_string(chat: Chat):
        chat_string = "=== CHAT WITH THE USER ===\n"
        for message in chat.chat_history:
            role = message['role']
            message = message['content']
            chat_string += f"{role}: {message}\n"
        chat_string += "=== (END OF CHAT) ===\n\n"
        return chat_string

    @staticmethod
    def _construct_memory_string(memories):
        if not memories:
            return ""
        memory_string = "=== AVAILABLE INFORMATION ===\n"
        for memory in memories:
            memory_string += f"{memory}"
        memory_string += "\n"
        return memory_string

    def build_request(self, details=None, method=None, instructions=None, chat: Chat = None, memories: list[str] = None):
        """
        :param method: HTTP method to use (GET, POST, PUT, DELETE)
        :param details: Details about the API endpoint, including all RELEVANT information from the API Specification.
        :param instructions: List of instructions from the invoker that explains how to build the request
        :param chat: Chat object, used to see all messages in the chat
        :param memories: List of memories from the task
        :return:
        """

        system_message = "You are a request builder.\n\nYou will be given:\n- a description of an API endpoint " \
                         "delimited by \"===\"- Unstructured information delimited by \"---\"\n- Additional instructions " \
                         "from the user\n\nCarefully examine the given information and create the filled in objects " \
                         "that should be sent to the api.\n\nUse the following structure for your answer:\n{\"url\": " \
                         "<full url including parameters>, \"json\": <filled json data>}\n\nYour answer should be " \
                         "loadable using Python's json.loads()."

        user_message = f"API Endpoint:\n===\n{details}"
        user_message += "\n===\n\nUnstructured information:\n---\n"
        if memories:
            user_message += self._construct_memory_string(memories)
        if chat:
            user_message += self._construct_chat_string(chat)

        if instructions:
            user_message += "---\n\nAdditional instructions:\n"
            user_message += instructions

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

        result = self.openai_client.chat_completion(
            messages=messages,
            model="gpt-4",
        )

        try:
            json_data = json.loads(result)
            url = json_data.get("url", "")
            _json = json_data.get("json", {})
            return url, _json
        except Exception as e:
            raise Exception(f"Failed to parse response from OpenAI: {e}", result)
