from openai import OpenAI
import os

import threading
from queue import Queue

import dotenv

dotenv.load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class OpenAIQuery:
    def __init__(self, messages, model, query_type="chat_completion"):
        self.done = threading.Event()
        self.exception = None
        self.result = None
        self.messages = messages
        self.model = model
        self.query_type = query_type


class OpenAIClient:
    """
    Responsible for calling OpenAI API and returning the results
    This is done using a queue,
    and in a way that respects the rate limits of the API.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:  # Singleton
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, max_workers: int = 30):
        if hasattr(self, '_initialized'):  # Singleton
            return
        self._initialized = True

        self.max_workers = max_workers

        self.current_queries = set()
        self.query_queue = Queue()

        self._init_worker_threads()

    def _init_worker_threads(self):
        for _ in range(self.max_workers):
            worker = threading.Thread(target=self._worker)
            worker.setDaemon(True)
            worker.start()

    def _worker(self):
        while True:
            query = self.query_queue.get()
            try:
                if not query:
                    continue
                if query in self.current_queries:
                    continue
                self.current_queries.add(query)
                self._query(query)
            except Exception as e:
                query.exception = e
                query.done.set()

    def _query(self, query: OpenAIQuery):
        """
        Queries OpenAI API
        :param query:
        :return:
        """
        # TODO: Add rate limiting and retry with exponential backoff
        # TODO: https://platform.openai.com/docs/guides/rate-limits/error-mitigation
        try:
            if query.query_type == "chat_completion":

                print(f"[OPENAI Query]\nModel: {query.model}\n{query.messages}")

                response = client.chat.completions.create(model=query.model,
                                                          messages=query.messages)
                query.result = response
                query.done.set()
            else:
                raise NotImplementedError(f"Query type {query.query_type} not implemented")
        except Exception as e:
            query.exception = e
            query.done.set()

    def chat_completion(self, messages, model):
        # Create query
        query = OpenAIQuery(messages, model, query_type="chat_completion")

        # Add query to queue
        self.query_queue.put(query)

        # Wait for query to finish
        query.done.wait()

        # Remove query from current queries
        self.current_queries.remove(query)

        # Check if there was an exception
        if query.exception:
            raise query.exception

        # Return result
        return query.result.choices[0].message.content
