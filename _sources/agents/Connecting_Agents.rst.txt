Agent Connection Availability
=============================

In our framework, agents can be interconnected to enhance their capabilities and access specialized functionalities.
This interconnectivity is managed through the `connections_available` attribute derived from the Agent superclass.

Understanding `connections_available`
--------------------------------------

The `connections_available` attribute is a dictionary that defines potential connections to other agents. Each key in this dictionary represents the ID of a child agent, indicating that the parent agent can delegate tasks or request information from these child agents. This setup allows for more in-depth and specialized information retrieval.

For instance, a weather agent might connect with agents specialized in humidity, wind, and precipitation data.

Example: DemoWeatherAgent
--------------------------

The `DemoWeatherAgent` is an example of an agent utilizing the `connections_available` attribute. This agent can connect with other agents specialized in various aspects of weather data.

.. code-block:: python

    class DemoWeatherAgent(Agent):
        """
        A weather agent that retrieve weather information.
        """
        def __init__(self):
            super().__init__(
                agent_id='demo_weather_agent',
                short_description='Fetch weather data',
                long_description='Fetch weather data',
                display_name='WEATHER',
                connections_available={
                    "humidity_agent": {},
                    "wind_agent": {},
                    "precipitation_agent": {}
                }
            )

In this example, `DemoWeatherAgent` is configured with connections to `humidity_agent`, `wind_agent`, and `precipitation_agent`. These connections allow `DemoWeatherAgent` to access more specific weather-related data, enhancing its overall functionality.

Conclusion
----------

Utilizing `connections_available`, agents in our framework can be interconnected to form a network of specialized functionalities. This design fosters a modular and flexible approach to building complex systems where agents can collaborate to achieve more comprehensive and detailed results.

Next Steps
----------

- Go further to learn how Agents communicate and use memories in the :doc:`How_Agents_Communicate_&_Memories` guide.
