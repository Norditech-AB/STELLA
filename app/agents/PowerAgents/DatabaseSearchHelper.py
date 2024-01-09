from app.models.agent import Agent
from app.models.chat import Chat
from app.openai_client import OpenAIClient
from app.utils.request_builder import RequestBuilder

from datetime import datetime


class DatabaseWriterHelper(Agent):

    # This is a custom instruction for the respond function. It is not used by the default Agent class.
    custom_instruction = "You are a database information finder. You will be given a JSON database and a chat between " \
                         "a User and the Assistant. Focus on the latest chat history between the User and the " \
                         "Assistant and find information related to the user's request.\n\nYour response should " \
                         "include useful information related to the user's request in a list. Your response should " \
                         "only contain the final list, nothing else. For example:\n- There exists <amount> of <item " \
                         "type> with <details>,\n- <field details> contains <items> with <item-details>\n- An <item> " \
                         "with <details> exists\n- There are no items of <item type> in the database\n- <item> with " \
                         "<details> does not exist"

    def __init__(self):
        super().__init__(
            agent_id='stella/database_search_helper',
            name='Database Search Helper',
            short_description='Can search the database for information',
            skip_action_selection=True,
            forward_all_memory_entries_to_parent=False,
            forward_last_memory_to_parent=True,
            model_for_response='gpt-4-1106-preview',
        )

    @staticmethod
    def _construct_chat_string(chat: Chat):
        chat_string = "=== CHAT WITH THE USER ===\n"
        for message in chat.chat_history:
            role = message['role']
            message = message['content']
            chat_string += f"{role}: {message}\n"
        chat_string += "=== (END OF CHAT) ==="
        return chat_string

    def respond(self, openai_client: OpenAIClient, request_builder: RequestBuilder, chat: Chat = None, memories=None):
        # 1. Describe what the user wants to do with the database
        # 2. Open the database
        # 3. Pass the entire json file to OpenAI and update anything that needs updating
        # 4. Save the updated json file
        # 5. Build an explanation of the updates
        # 6. Return the explanation
        import os
        this_folder = os.path.dirname(os.path.abspath(__file__))
        import json
        database = {}
        # If there's no database, create one
        if not os.path.exists(this_folder + "/database.json"):
            with open(this_folder + "/database.json", "w") as outfile:
                json.dump(database, outfile)
        # Open the database
        with open(this_folder + "/database.json") as json_file:
            database = json.load(json_file)

        # Build user history string
        history_string = f"{self._construct_chat_string(chat) if chat else ''}"

        # Build database string
        original_database_string = json.dumps(database)
        database_string = f"=== DATABASE ===\n{original_database_string}\n=== (END OF DATABASE) ==="

        user_string = f"{history_string}\n\n{database_string}\n\n{self.custom_instruction}"

        # Pass the entire json file to OpenAI and search for information
        messages = [
            {
                "role": "system",
                "content": self.custom_instruction
            },
            {
                "role": "user",
                "content": user_string
            }
        ]

        database_search = openai_client.chat_completion(
            messages=messages,
            model=self.model_for_response,
        )

        current_time = datetime.now().strftime("%-d %b %H:%M")

        return f"{current_time} - Database Search Helper search results:\n{database_search}"
