============================
Creating a New Agent
============================

This document explains how to create a new agent based on the `Agent` superclass.

Introduction
------------

Creating a new agent involves subclassing from the `Agent` superclass and implementing specific methods to customize the agent's behavior.

Prerequisites
-------------

- Basic knowledge of Python programming
- Familiarity with the `Agent` superclass structure
- Setup of the necessary environment for running agents

Steps to Create a New Agent
---------------------------

For clarity we use the **DemoWeatherAgent** class as an example. This agent uses an API to fetch weather data for a given city. The agent's response is a string containing the weather data.
These steps are based on the **DemoWeatherAgent** class in the `app/models/agent/demo_weather_agent.py` file.

1. Import the Necessary Modules
-------------------------------

.. code-block:: python

    import requests
    from app.models.agent import Agent
    from app.models.chat import Chat
    from app.openai_client import OpenAIClient
    from app.utils.request_builder import RequestBuilder

2. Define the New Agent Class
-----------------------------

.. code-block:: python

    class DemoWeatherAgent(Agent):
        """
        A weather agent that uses an API to get weather information.
        """

3. Initialize the Agent
-----------------------

Override the `__init__` method to set up the agent's basic attributes.

.. code-block:: python

    def __init__(self):
        super().__init__(
            agent_id='demo_weather_agent',
            name='WEATHER',
            short_description='Fetch weather data',
            ...
        )

4. Implement the `respond` Method
---------------------------------

This method is responsible for generating the agent's response. For example if other agents are involved in the conversation, the agent can use the `memories` parameter to access the other agents' responses.

.. code-block:: python

    def respond(self, openai_client: OpenAIClient, request_builder: RequestBuilder, chat: Chat = None, memories=None):
        ...

.. note::
    Read more about the `respond` method in the :doc:`How_Agents_Communicate_&_Memories` documentation.

5. Define Additional Helper Methods
------------------------------------

Include any additional methods needed for your agent's functionality.

.. code-block:: python

    def get_lat_long(self, city):
        ...

    def get_weather(self, city):
        ...

Key Methods in the Custom Agent
-------------------------------

- `__init__`: Initializes the agent with specific attributes.
- `respond`: Handles the creation of the agent's response.
- `get_lat_long`: Helper method to fetch latitude and longitude.
- `get_weather`: Helper method to retrieve weather data.

Conclusion
----------

By following these steps and using the `Agent` superclass as a base, you can create a variety of specialized agents tailored to specific tasks or functionalities.
