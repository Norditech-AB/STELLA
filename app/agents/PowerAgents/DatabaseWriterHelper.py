from app.models.agent import Agent
from app.models.chat import Chat
from app.openai_client import OpenAIClient
from app.utils.request_builder import RequestBuilder

from datetime import datetime


class DatabaseManagerAgent(Agent):

    # This is a custom instruction for the respond function. It is not used by the default Agent class.
    custom_instruction = "You are a database manager. You will be given a list of historical actions and a chat " \
                         "history between the User and the Assistant. You will also be provided with the current " \
                         "database in a JSON format. Focus on the latest chat history between the User and the " \
                         "Assistant and update the database to fulfill the User's request. You are allowed to do " \
                         "anything with the database, such as create new keys, update existing keys, update any " \
                         "values etc.\n\nRespond with the updated database in a JSON string. Your response should " \
                         "ONLY include the final (full) database as a json string. Your response should not include" \
                         " any custom formatting such as markdown or indentation." \
                         " Your response must be loadable using Python's json.loads() function."

    system_response_instructions = "You will be given two versions of a JSON database. The first one is the original, " \
                                   "and the second one is the updated version after changes has been made.\n\nYour " \
                                   "task is to identify and explain the changes that have been made in the " \
                                   "database.\n\nYour response should be a list of the updates that have " \
                                   "been made in a list. Your response should only contain the final list, " \
                                   "nothing else. For example:\n- Added new item with <details>to the field " \
                                   "<field name> successfully,\n- Updated <field name> <item> with <details> " \
                                   "successfully\n- Deleted <field name> <item> successfully" \


    def __init__(self):
        super().__init__(
            agent_id='stella/database_writer_helper',
            name='Database Writer Helper',
            short_description='Can update anything in the database (write, create, update, delete)',
            skip_action_selection=True,
            forward_all_memory_entries_to_parent=False,
            forward_last_memory_to_parent=True,
            system_response_instructions=self.system_response_instructions,
            model_for_response='gpt-4-1106-preview',
        )

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
        history_string = f"{self._construct_memory_string(memories) if memories else ''}\n" \
                         f"{self._construct_chat_string(chat) if chat else ''}"

        # Build database string
        original_database_string = json.dumps(database)
        database_string = f"=== DATABASE ===\n{original_database_string}\n=== (END OF DATABASE) ==="

        user_string = f"{history_string}\n\n{database_string}\n\n{self.custom_instruction}"

        # Pass the entire json file to OpenAI and update anything that needs updating
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

        updated_database_string = openai_client.chat_completion(
            messages=messages,
            model=self.model_for_response,
        )

        # Clean up potential formatting
        updated_database_string = updated_database_string.replace("```json", "").replace("```", "").strip()

        # Convert the json string to a dictionary
        update_database = json.loads(updated_database_string)

        # Save the updated json file
        with open(this_folder + "/database.json", "w") as outfile:
            json.dump(update_database, outfile)

        # Build an explanation of the updates
        response_messages = [
            {
                "role": "system",
                "content": self.system_response_instructions
            },
            {
                "role": "user",
                "content": f"Original JSON database\n{original_database_string}\n\nUpdated JSON database{updated_database_string}"
            }
        ]

        response = openai_client.chat_completion(
            messages=response_messages,
            model=self.model_for_response,
        )

        current_time = datetime.now().strftime("%-d %b %H:%M")

        return f"{current_time} - Database Writer Helper updated database:\n{response}"
