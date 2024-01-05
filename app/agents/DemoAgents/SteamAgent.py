import requests

from app.models.agent import Agent
from app.models.chat import Chat
from app.openai_client import OpenAIClient
from app.utils.request_builder import RequestBuilder


class SteamAgent(Agent):
    """
    A Steam agent that uses an API to get steam information.
    """
    def __init__(self):
        super().__init__(
            agent_id='steam_agent',
            name='STEAM',
            short_description='Fetch Steam data for a specific Game',
            forward_all_memory_entries_to_parent=True,
            skip_action_selection=True,
        )
    
    custom_system_response_instructions = "\n\n==== INSTRUCTIONS ====\n" \
                                          "Your name is Steam-Agent. You are an AI assistant used to fetch steam data" \
                                          "\n\nGenerate an appropriate response to " \
                                          "the user's request using the provided details. Focus on the user's latest " \
                                          "message, and use the provided details to respond in a proper manner. Don't " \
                                          "lie or make things up. Be as helpful, nice and concise as possible."


    @staticmethod
    def get_app_id(name: str) -> str:
        api_url = f"https://api.steampowered.com/ISteamApps/GetAppList/v2/"
        print("[AGENT] Constructed API URL: " + api_url)

        response = requests.get(api_url)
        if response.status_code != 200:
            return "Error in Open-Meteo API request – Tell the user that something went wrong and stop the conversation"
        steam_data = response.json()
        print("-----------------STEAM------------------")
        print(steam_data)
        print("-----------------STEAM------------------")

        for app in steam_data["applist"]["apps"]:
            if app["name"] == name:
                return app["appid"]

        return "Error in Open-Meteo API request – Tell the user that something went wrong and stop the conversation"

    @staticmethod
    def get_player_count(api_key: str, game: str) -> str:
        appid = SteamAgent.get_app_id(game)

        api_url = f"https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={appid}&key={api_key}"

        print("[AGENT] Constructed API URL: " + api_url)

        response = requests.get(api_url)
        if response.status_code != 200:
            return "Error in Open-Meteo API request – Tell the user that something went wrong and stop the conversation"
        steam_data = response.json()
        print("-----------------STEAM------------------")
        print(steam_data)
        print("-----------------STEAM------------------")

        return f"Tell the user that the game '{game} currently has {steam_data['response']['player_count']} online players and add some trivia about the game and stop the conversation"

    def respond(self, openai_client: OpenAIClient, request_builder: RequestBuilder, chat: Chat = None, memories=None):

        user_message = f"{self._construct_memory_string(memories) if memories else ''}" \
                       f"{self._construct_chat_string(chat) if chat else ''}" \
                       f"{self.system_response_instructions}"

        key_messages = [
            {
                "role": "system",
                "content": "Extract the API key from the user's message. Only respond with the API key, nothing else. No other text. Only the key itself. If you can't find an API-key, just respond with nothing."
            },
            {
                "role": "user",
                "content": user_message
            }
        ]

        print(f"[AGENT] {self.name} is responding using OpenAI: {key_messages}")

        key = openai_client.chat_completion(
            messages=key_messages,
            model=self.model_for_response,
        )

        if key == "":
            return "Tell the user that the API key is missing and stop the conversation"

        game_messages = [
            {
                "role": "system",
                "content": "Extract the name of the game from the user's message. Only respond with the name of the game, nothing else"
            },
            {
                "role": "user",
                "content": user_message
            }
        ]


        game = openai_client.chat_completion(
            messages=game_messages,
            model=self.model_for_response,
        )
        print(f"{key=}, {game=}")
        # Step 3: Respond
        return SteamAgent.get_player_count(key, game)
