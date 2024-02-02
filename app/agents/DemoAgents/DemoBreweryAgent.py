import requests

from app.models.agent import Agent
from app.models.chat import Chat
from app.openai_client import OpenAIClient
from app.utils.request_builder import RequestBuilder


class DemoBreweryAgent(Agent):
    """
    A brewery agent that uses an API to get breweries from cities, mainly from USA.
    """
    def __init__(self):
        super().__init__(
            agent_id='demo_brewery_agent',
            name='BREWERY',
            short_description='Fetch brewery data',
            forward_all_memory_entries_to_parent=True,
            skip_action_selection=True,
            max_depth=2,
        )

    @staticmethod
    def get_brewery(city: str) -> object:
        if not city:
            return "Error in OpenStreetMap API request – Tell the user that something went wrong and stop the conversation"

        # Get the weather using Open-Meteo
        brewery_url = f"https://api.openbrewerydb.org/v1/breweries?by_city={city}&per_page=200"
        brewery_response = requests.get(brewery_url)
        if brewery_response.status_code != 200:
            return "Error in Open-Meteo API request – Tell the user that something went wrong and stop the conversation"
        
        brewery_data = brewery_response.json()

        return brewery_data

    def respond(self, openai_client: OpenAIClient, request_builder: RequestBuilder, chat: Chat = None, memories=None):
        user_message = f"{self._construct_memory_string(memories) if memories else ''}" \
                       f"{self._construct_chat_string(chat) if chat else ''}" \
                       f"{self.system_response_instructions}"

        messages = [
            {
                "role": "system",
                "content": "Extract the city from the user's message. Respond with the city name eg \"Miami\", nothing else}"
            },
            {
                "role": "user",
                "content": user_message
            }
        ]

        print(f"[AGENT] {self.name} is responding using OpenAI: {messages}")
        
        city = openai_client.chat_completion(
            messages=messages, 
            model=self.model_for_response
        )
        city = city.replace(".", "").replace(",", "").replace("!", "").replace("?", "").replace(":", "").replace(";", "").replace("\"", "").replace("'", "").replace("'", "").replace("'", "").replace(""", "").replace(""", "").replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace("{", "").replace("}", "").replace("-", "").replace("_", "").replace("+", "").replace("=", "").replace("/", "").replace("\\", "").replace("|", "").replace("<", "").replace(">", "").replace("#", "").replace("*", "").replace("~", "").replace("`", "").replace("@", "")

        # Get the weather
        breweries = self.get_brewery(city)

        # Respond
        if not breweries:
            return f"The database does not support the city {city}"
        return f"The data about breweries in the city {city} are {breweries}. Clean this up so the response fits the request."
