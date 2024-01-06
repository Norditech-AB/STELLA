import textwrap
import threading

import requests

from app.models.agent import Agent
from app.models.chat import Chat
from app.openai_client import OpenAIClient
from app.utils.request_builder import RequestBuilder
from openai import OpenAI
import pygame
import concurrent.futures
class StellaMMORPG(Agent):
    """
    A mmorpg game.
    """
    def __init__(self):
        super().__init__(
            agent_id='stella/stella_mmo_rpg',
            name='StellaMMORPG',
            short_description='The Stella MMORPG game. ',
            forward_all_memory_entries_to_parent=False,
            forward_last_memory_to_parent=False,
            skip_action_selection=True,
            skip_response=True,
            max_depth=1,
            on_completion=self.init_game,
        )
        self.client = OpenAI()

    def init_game(self, socketio=None , chat_id = None, chat: Chat = None, memories=None, openai_client: OpenAIClient = None):
        user_input = f"{self._construct_chat_string(chat) if chat else ''}"
        self.create_character_image(user_input, openai_client)
        print(f"[STELLA MMORPG] {self.name} is responding using OpenAI: {user_input}")
        character_story = self.create_character_story(openai_client, user_input)
        print(f"[STELLA MMORPG] {self.name} created character: {character_story}")
        self.start_game_thread(character_story)
        print(f"[STELLA MMORPG] {self.name} started game thread: {character_story}")
        # self.display_character(character_story)
        # print(f"[STELLA MMORPG] {self.name} displayed character: {character_story}")
        print("[STELLA MMORPG] Game started successfully. Running in the background...")

    def create_character_story(self, openai_client: OpenAIClient, user_input: str):
        messages = [
            {
                "role": "system",
                "content": "You are a role playing leader. You are creating a character for a user. Please provide details like name, class, and race. Maximum 50 words."
            },
            {
                "role": "user",
                "content": user_input
            }
        ]

        print(f"[STELLA MMORPG] Creating character with: {messages}")

        response = openai_client.chat_completion(
            messages=messages,
            model=self.model_for_response,
        )

        return response

    def display_character(self, character_story):
        # Initialize Pygame
        pygame.init()

        # Set up the display
        screen_width, screen_height = 800, 600
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("StellaMMORPG")

        # Load images
        avatar_image = pygame.image.load('C:/Users/Fredr/Documents/stella-open-source/STELLA/app/generated_avatar.png')  # Replace with the path to the avatar image
        forest_image = pygame.image.load('C:/Users/Fredr/Documents/stella-open-source/STELLA/app/2d_forest.png')  # Replace with the path to the forest image

        # Scale images to fit the screen (optional)
        avatar_image = pygame.transform.scale(avatar_image, (250, 250))  # Example size, adjust as needed
        forest_image = pygame.transform.scale(forest_image, (screen_width, screen_height))

        # Font setup for story text
        font = pygame.font.SysFont(None, 24)
        text_color = (255, 255, 255)  # White text, change as needed
        wrapped_text = textwrap.wrap(character_story, width=50)  # Adjust width as needed

        # Calculate text block height
        text_block_height = len(wrapped_text) * (font.get_height() + 2) + 20  # Adjust padding as needed

        # Game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Draw the forest background
            screen.blit(forest_image, (0, 0))

            # Draw the avatar
            avatar_position = (screen_width // 2, screen_height // 2)  # Center the avatar, adjust as needed
            screen.blit(avatar_image, avatar_position)

            # Draw a semi-transparent rectangle behind the text
            text_block = pygame.Surface((screen_width - 40, text_block_height))  # Adjust width as needed
            text_block.set_alpha(128)  # Adjust alpha for transparency (0-255)
            text_block.fill((0, 0, 0))  # Black color, change as needed
            screen.blit(text_block, (20, 150))  # Adjust position as needed

            # Draw the character story
            y_offset = 160  # Starting y position for the story text, adjust as needed
            for line in wrapped_text:
                text_surface = font.render(line, True, text_color)
                screen.blit(text_surface, (30, y_offset))
                y_offset += text_surface.get_height()  # Move to the next line

            # Update the display
            pygame.display.flip()

        pygame.quit()

    def create_character_image(self, description, openai_client):
        # Format the prompt for the API
        prompt = f"Create an avaatar image of a character described as follows: {description}"

        print(f"[STELLA MMORPG] Creating character with: {prompt}")

        response = self.client.images.generate(
          model="dall-e-3",
          prompt=prompt,
          size="1024x1024",
          quality="standard",
          n=1,
        )

        print(f"[Dall-e] Response: ", response)
        print("[Dall-e] Response url: ", response.data[0].url)

        # Assuming the API returns a direct link to the image
        image_url = response.data[0].url

        # Download and save the image
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            # Save the image to the project's root folder
            with open(f'C:/Users/Fredr/Documents/stella-open-source/STELLA/app/generated_avatar.png', 'wb') as file:
                file.write(image_response.content)
            return "Image saved successfully."
        else:
            return "Failed to download the image."

    def start_game_thread(self, character_story):
        # Create a thread for the Pygame window
        try:
            game_thread = threading.Thread(target=self.display_character, args=(character_story,))
            game_thread.daemon = True
            game_thread.start()
        except Exception as e:
            print(f"[STELLA MMORPG] Failed to start game thread: {e}")

    def respond(self, openai_client: OpenAIClient, request_builder: RequestBuilder, chat: Chat = None, memories=None):

        # Step 3: Respond
        return "The Stella MMORPG game is finished."
