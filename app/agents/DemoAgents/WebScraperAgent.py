import requests
from bs4 import BeautifulSoup

from app.models.agent import Agent
from app.models.chat import Chat
from app.openai_client import OpenAIClient
from app.utils.request_builder import RequestBuilder


class DemoWebScrapingAgent(Agent):
    """
    A web scraping agent that extracts data from a specified website.
    """
    def __init__(self):
        super().__init__(
            agent_id='demo_web_scraping_agent',
            name='WEB_SCRAPER',
            short_description='Scrape data from a specific website',
            forward_all_memory_entries_to_parent=True,
            skip_action_selection=True,
            max_depth=3
        )

    def scrape_website(self, url):
        """
        Scrape the given URL for data.
        :param url: The URL to scrape.
        :return: Scraped data or error message.
        """
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                data = soup.get_text(separator=' ', strip=True)  
                return f"Scraped data: {data}"
            else:
                return "Error accessing the website"
        except Exception as e:
            return f"An error occurred: {e}"

    def respond(self, openai_client: OpenAIClient, request_builder: RequestBuilder, chat: Chat = None, memories=None):

        # You can modify this section to extract a URL from user input if needed
        user_message = f"{self._construct_memory_string(memories) if memories else ''}" \
                       f"{self._construct_chat_string(chat) if chat else ''}" \
                       f"{self.system_response_instructions}"

        messages = [
            {
                "role": "system",
                "content": "Extract the url from the user's message and provided details. Only respond with the url name, e.g. \"https://www.scrapingbee.com/tutorials\", nothing else."
            },
            {
                "role": "user",
                "content": user_message
            }
        ]

        print(f"[AGENT] {self.name} is responding using OpenAI: {messages}")

        url = openai_client.chat_completion(
            messages=messages,
            model=self.model_for_response,
        )

        # Step 1: Scrape the website
        scraped_data = self.scrape_website(url)

        # Step 2: Respond with the scraped data or an error message
        return scraped_data
