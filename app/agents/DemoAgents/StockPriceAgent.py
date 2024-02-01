import yfinance as yf

from app.models.agent import Agent
from app.models.chat import Chat
from app.openai_client import OpenAIClient
from app.utils.request_builder import RequestBuilder


class StockPriceAgent(Agent):
    """
    A stock price agent that uses yfinance to get stock price information.
    """
    def __init__(self):
        super().__init__(
            agent_id='stock_price_agent',
            name='STOCK_PRICE',
            short_description='Fetch stock price data',
            forward_all_memory_entries_to_parent=True,
            skip_action_selection=True,
        )

    def get_stock_price(self,symbol):
        try:
            # Fetch stock data
            stock = yf.Ticker(symbol)
            
            # Get the most recent closing price
            price = stock.history(period='1min')['Close'][0]
            
            return price
        except Exception as e:
            print(e)
            return "Error in yfinance API request – Tell the user that something went wrong or maybe the ticker does not exist and stop the conversation"

    def respond(self, openai_client: OpenAIClient, request_builder: RequestBuilder, chat: Chat = None, memories=None):
        user_message = f"{self._construct_memory_string(memories) if memories else ''}" \
                       f"{self._construct_chat_string(chat) if chat else ''}" \
                       f"{self.system_response_instructions}"

        messages = [
            {
                "role": "system",
                "content": "Extract the stock symbol from the user's message and provided details. Only respond with the stock symbol, e.g., \"AAPL\", nothing else."
            },
            {
                "role": "user",
                "content": user_message
            }
        ]

        print(f"[AGENT] {self.name} is responding using OpenAI: {messages}")

        # Use OpenAI to extract stock symbol from the user's message
        symbol = openai_client.chat_completion(
            messages=messages,
            model=self.model_for_response,
        )

        symbol.replace(".", "").replace(",", "").replace("!", "").replace("?", "").replace(":", "").replace(";", "").replace("\"", "").replace("'", "").replace("’", "").replace("‘", "").replace("“", "").replace("”", "").replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace("{", "").replace("}", "").replace("-", "").replace("_", "").replace("+", "").replace("=", "").replace("/", "").replace("\\", "").replace("|", "").replace("<", "").replace(">", "").replace("#", "").replace("*", "").replace("~", "").replace("`", "").replace("@", "")

        # Get the stock price
        stock_price = self.get_stock_price(symbol)

        # Respond with the stock price
        return f"The price of {symbol} stock is {stock_price}"