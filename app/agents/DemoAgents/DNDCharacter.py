import requests

from app.models.agent import Agent
from app.models.chat import Chat
from app.openai_client import OpenAIClient
from app.utils.request_builder import RequestBuilder

class DnDCharacterCreationAgent(Agent):
    """
    An agent that uses the D&D 5e SRD API to help create D&D characters. # https://5e-bits.github.io/docs/
    """
    def __init__(self):
        super().__init__(
            agent_id='dnd_character_agent',
            name='DnDCharacterCreator',
            short_description='Create D&D characters',
            forward_all_memory_entries_to_parent=True,
            skip_action_selection=True,
            max_depth=2,
        )

    def get_resources(self):
        url = "https://www.dnd5eapi.co/api"

        payload = {}
        headers = {
        'Accept': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        return response.text

    def get_lower_level_resources(self, resource):
        url = f"https://www.dnd5eapi.co/api/{resource}"

        payload = {}
        headers = {
        'Accept': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code == 200:
            return response.text
        else:
                # Handle errors
                if response.status_code == 404:
                    return "Resource not found."
                elif response.status_code == 500:
                    return "Internal server error. Please try again later."
                else:
                    return f"An error occurred: {response.status_code}"


    def respond(self, openai_client: OpenAIClient, request_builder: RequestBuilder, chat: Chat = None, memories=None):
        user_message = f"{self._construct_memory_string(memories) if memories else ''}" \
                       f"{self._construct_chat_string(chat) if chat else ''}" \
                       f"{self.system_response_instructions}"

        messages = [
            {
                "role": "system",
                "content": f"Extract a setting of these options alignment, races, classes,language,deception, and backgrounds, \
                    select one which the user needs to start or continue with the character creation. Respond ONLY with one of the settings e.g \"races\" or the word \"settings\", if no appropiate setting cna be found"
            },
            {
                "role": "user",
                "content": user_message
            }
        ]

        print(f"[AGENT] {self.name} is responding using OpenAI: {messages}")

        resource = openai_client.chat_completion(
            messages=messages,
            model=self.model_for_response,
        )

        resource.replace(".", "").replace(",", "").replace("!", "").replace("?", "").replace(":", "").replace(";", "").replace("\"", "").replace("'", "").replace("'", "").replace("'", "").replace(""", "").replace(""", "").replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace("{", "").replace("}", "").replace("-", "").replace("_", "").replace("+", "").replace("=", "").replace("/", "").replace("\\", "").replace("|", "").replace("<", "").replace(">", "").replace("#", "").replace("*", "").replace("~", "").replace("`", "").replace("@", "")

        # Step 2: Get the weather
        
        settings = "alignment, races, classes,language,deception, and backgrounds"
        # Step 3: Respond
        if resource == "settings":
            return f"These are the settings available for selections {settings}"
        l_resource = self.get_lower_level_resources(resource)
        return f"you can choose a characteristic to the character from this data {l_resource}"


