import requests

from app.models.agent import Agent
from app.models.chat import Chat
from app.openai_client import OpenAIClient
from app.utils.request_builder import RequestBuilder
import time
import sys

class StellaCactusAgent(Agent):
    """
    A simple agent that tells a story about Stella the cactus and Fred the balloon.
    """
    def __init__(self):
        super().__init__(
            agent_id='stella/stella_cactus_agent',
            name='StellaCactus',
            short_description='Tell a story about Stella the cactus and Fred the balloon',
            forward_all_memory_entries_to_parent=False,
            forward_last_memory_to_parent=False,
            skip_action_selection=True,
            skip_response=True,
            max_depth=1,
            on_completion = self.scroll_text
        )


    def scroll_text(self, socketio, chat_id, **kwargs):
        """
        Scrolls the given text in the command line with a specified delay.

        Args:
        text (str): The text to scroll.
        delay (float): The time delay (in seconds) between each line.
        """
        text = """
            In the vast and sun-drenched expanse of the Whimsical Desert, there thrived an extraordinary cactus named Stella. 
            Stella was no ordinary cactus; she had a heart brimming with adventure and a most unusual best friend 
            - a balloon named Fred. 
            Fred, resilient and cheerful, adored Stella, and in their unique world, they were inseparable companions. #

            Together, they embarked on whimsical adventures, 
            from fishing in the mirage lakes of the desert 
            - with Stella's thorns cleverly serving as fishing hooks 
            - to Fred gracefully floating above, watching over their playful endeavors. #

            They spent nights star gazing, days racing with the desert winds, 
            and evenings sharing tales under the moonlight. 
            As they gazed up at the twinkling stars, Stella and Fred would often speak of their most hopeful dream. 
            In the quiet of the desert night, they shared a mutual longing, a wish they held closest to their hearts #
            
            - the dream to one day embrace each other in a hug. 
            It was a dream filled with longing and hope, 
            a moment they believed would encapsulate the essence of their deep and unbreakable bond. #
            
            For Stella and Fred, their friendship was as natural as the desert's shifting sands, 
            and this dream of a simple hug became their shared beacon of hope in the vastness of the Whimsical Desert.
            
            """
        delay = 1.3
        extended_delay = 3.5

        for line in text.split('\n'):
            if '#' in line:
                # Remove the '#' character and then emit the line
                line_without_hash = line.replace('#', '')
                socketio.emit('message', line_without_hash, room=chat_id, namespace='/chat')
                time.sleep(extended_delay)
            else:
                socketio.emit('message', line, room=chat_id, namespace='/chat')
                time.sleep(delay)

    def respond(self, openai_client: OpenAIClient, request_builder: RequestBuilder, chat: Chat = None, memories=None):

        return f"The storytelling of Stella and Fred is done."
