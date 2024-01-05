import requests

from app.models.agent import Agent
from app.models.chat import Chat
from app.openai_client import OpenAIClient
from app.utils.request_builder import RequestBuilder


class DemoWeatherAgent(Agent):
    """
    A weather agent that uses an API to get weather information.
    """
    def __init__(self):
        super().__init__(
            agent_id='demo_weather_agent',
            name='WEATHER',
            short_description='Fetch weather data',
            forward_all_memory_entries_to_parent=True,
            skip_action_selection=True,
        )

    def get_lat_long(self, city):
        """
        Thanks to the OpenStreetMap API, we can get the latitude and longitude of a city.
        © OpenStreetMap contributors
        :param city:
        :return:
        """
        url = f"https://nominatim.openstreetmap.org/search?city={city}&format=json"
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            data = response.json()
            if data:
                latitude = data[0]['lat']
                longitude = data[0]['lon']
                return latitude, longitude
            else:
                return None, None
        else:
            return None, None

    def get_weather(self, city):
        print(city)
        # Step 1: Get the latitude and longitude of the city
        latitude, longitude = self.get_lat_long(city)

        if not latitude or not longitude:
            return "Error in OpenStreetMap API request – Tell the user that something went wrong and stop the conversation"

        # Step 2: Get the weather using Open-Meteo
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
        weather_response = requests.get(weather_url)
        if weather_response.status_code != 200:
            return "Error in Open-Meteo API request – Tell the user that something went wrong and stop the conversation"
        weather_data = weather_response.json()

        # Step 3: Extract and return the relevant data
        current_weather = weather_data.get('current_weather', {})
        return current_weather

    def respond(self, openai_client: OpenAIClient, request_builder: RequestBuilder, chat: Chat = None, memories=None):

        user_message = f"{self._construct_memory_string(memories) if memories else ''}" \
                       f"{self._construct_chat_string(chat) if chat else ''}" \
                       f"{self.system_response_instructions}"

        messages = [
            {
                "role": "system",
                "content": "Extract the city from the user's message and provided details. Only respond with the city name, e.g. \"New York\", nothing else."
            },
            {
                "role": "user",
                "content": user_message
            }
        ]

        print(f"[AGENT] {self.name} is responding using OpenAI: {messages}")

        response = openai_client.chat_completion(
            messages=messages,
            model=self.model_for_response,
        )

        city = response['choices'][0]['message']['content']
        city.replace(".", "").replace(",", "").replace("!", "").replace("?", "").replace(":", "").replace(";", "").replace("\"", "").replace("'", "").replace("’", "").replace("‘", "").replace("“", "").replace("”", "").replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace("{", "").replace("}", "").replace("-", "").replace("_", "").replace("+", "").replace("=", "").replace("/", "").replace("\\", "").replace("|", "").replace("<", "").replace(">", "").replace("#", "").replace("*", "").replace("~", "").replace("`", "").replace("@", "")

        # Step 2: Get the weather
        weather = self.get_weather(city)

        # Step 3: Respond
        return f"The weather in {city} is {weather}"
