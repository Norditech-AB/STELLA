Connecting Agents
=================

In the STELLA framework, agents can be interconnected to enhance their capabilities and access specialized functionalities.
This interconnectivity is managed through the `connections_available` attribute derived from the Agent superclass.

Understanding `connections_available`
--------------------------------------

The `connections_available` attribute is a dictionary that defines potential connections to other agents. Each key in this dictionary represents the ID of a child agent, indicating that the parent agent can delegate tasks or request information from these child agents. This setup allows for more in-depth and specialized information retrieval.

For instance, a weather agent might connect with agents specialized in humidity, wind, and precipitation data.

Example: DemoWeatherAgent
--------------------------

Here is a version of the `DemoWeatherAgent` utilizing the `connections_available` attribute. This agent can delegate tasks to the other agents specialized in various aspects of weather data.

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

In this example, `DemoWeatherAgent` is configured with connections to `humidity_agent`, `wind_agent`, and `precipitation_agent`. If the `DemoWeatherAgent` is asked about humidity, it will delegate the task to the `humidity_agent` and return the result.

Next Steps
----------

- Go further to learn how Agents communicate and use memories in the :doc:`How_Agents_Communicate_&_Memories` guide.
