import Stella

#agents
agent = Stella.Agent(short_description("Fetch Weather data"))
agent = agent.agent_id = "hello"
agent.save("agent")


#define api
position_api = stella.API()

documentation = stella.api.Documentation("Get the weather of a city")
base_endpoint = stella.api.Endpoint("https://nominatim.openstreetmap.org/search")
auth_basic = Stella.Auth.basic_auth(username="user", password="pass")


position_api.add(documentation)
position_api.add(base_endpoint)
position_api.add(auth_basic)


agent.add(position_api)


#File handler
file_handler = Stella.file_handler(accept_files=[".png", '.jpg'], max_size=1000, description="Image of a cat")

agent.add(file_handler)
agent.add(position_api)


#load agent
agent = Stella.load_agent("my_agent.py")

#Create chats
chat = stella.Chat()
chat.add(agent)
chat.speak("Hello, what is the weather in jönköping", file="image.png")

another_chat = stella.Chat()
another_chat.add([agent1, agent2])
response = chat.speak("Hello, what is the weather in stockholm", wait_for_response=False)
print(response)

'''
model = keras.Sequential()
model.add(keras.Input(shape=(16,)))
model.add(keras.layers.Dense(8))

# Note that you can also omit the initial `Input`.
# In that case the model doesn't have any weights until the first call
# to a training/evaluation method (since it isn't yet built):
model = keras.Sequential()
model.add(keras.layers.Dense(8))
model.add(keras.layers.Dense(4))
# model.weights not created yet

# Whereas if you specify an `Input`, the model gets built
# continuously as you are adding layers:
model = keras.Sequential()
model.add(keras.Input(shape=(16,)))
model.add(keras.layers.Dense(8))
len(model.weights)  # Returns "2"

# When using the delayed-build pattern (no input shape specified), you can
# choose to manually build your model by calling
# `build(batch_input_shape)`:
model = keras.Sequential()
model.add(keras.layers.Dense(8))
model.add(keras.layers.Dense(4))
model.build((None, 16))
len(model.weights)  # Returns "4"

# Note that when using the delayed-build pattern (no input shape specified),
# the model gets built the first time you call `fit`, `eval`, or `predict`,
# or the first time you call the model on some input data.
model = keras.Sequential()
model.add(keras.layers.Dense(8))
model.add(keras.layers.Dense(1))
model.compile(optimizer='sgd', loss='mse')
# This builds the model for the first time:
model.fit(x, y, batch_size=32, epochs=10)
'''