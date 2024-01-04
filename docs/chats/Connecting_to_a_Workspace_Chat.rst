Connecting to a Workspace Chat
==============================

This documentation explains the process of connecting to a workspace chat in our framework, detailing how chats are created, connected to, and how messages are sent and received. The system uses the SocketIO library to manage chat connections and interactions.

Creating a Chat
---------------

A chat is created by making a POST request to the `/chat` endpoint. This process involves the following steps:

1. **Verifying User and Workspace:**
   The user's identity is verified, and the workspace ID is retrieved from the request.

2. **Workspace Existence Check:**
   The system checks if the specified workspace exists and if the user is the owner.

3. **Chat Creation:**
   A new chat object is created in the database.

.. note::
    See all the endpoints descriptions in the :doc:`../API_Reference`.

Connecting to a Chat
--------------------

To establish a connection to a chat, the client interacts with the `/connect` endpoint of the SocketIO server:

1. **Obtaining a Connection String:**
   The `get_connection_string()` function is called to generate a secret string used for validating chat connections.

2. **Connection Parameters:**
   The chat ID and a connection string are required to establish a connection.

3. **Connection String Verification:**
   The connection string is verified for authenticity and expiration.

4. **Chat and Workspace Validation:**
   The existence of the chat and its associated workspace is confirmed.

Underlying Connection Function
------------------------------

The underlying connection function utilizes the SocketIO library to handle the chat connection:

1. **Disconnecting if Already Connected:**
   If already connected to a chat, the client disconnects first.

2. **Establishing New Connection:**
   A new connection to the chat is established using the chat ID and the connection string.

3. **Session Update:**
   The session information is updated to reflect the new chat connection.

.. note::
   For more detailed information on the SocketIO library and its usage in Python, please refer to the official SocketIO documentation. The SocketIO library facilitates real-time bidirectional event-based communication, which is integral to the chat functionality in our framework. You can access the documentation at: `SocketIO official documentation <https://python-socketio.readthedocs.io/en/latest/>`_.


Message Handling in Chats
-------------------------

Every time a message is sent to a chat object, it must include a connection string for verification. The chat object compares this string to ensure the message is from an authorized source.

1. **Obtaining a Message String:**
   The `get_message_string()` function is invoked to generate a secret string for each message.

2. **Message Verification:**
   Upon receiving a message, the chat object checks if the message string matches.

3. **Message Processing:**
   If the message string is valid, the message is processed; otherwise, it is ignored or rejected.

Conclusion
----------

The process of creating, connecting to, and interacting within a workspace chat is integral to our framework. It ensures secure and verified communication between users and workspaces, facilitated by the SocketIO library.

Next Steps
----------

- Learn how the system sends and receives messages in the :doc:`Sending_and_Receiving_Messages` section.
