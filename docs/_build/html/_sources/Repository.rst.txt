Repository
==========

Project Structure
-----------------

The project is structured as follows:

- :file:`app/`: contains the STELLA flask socketio application
- :file:`cli/`: contains the STELLA CLI

STELLA Application (app/)
~~~~~~~~~~~~~~~~~~~~~~~~~

The flask application is structured as follows:

- :file:`run.py`: the main entry point for the application
- :file:`agents/`: contains agents that are used by the application
- :file:`models/`: base classes
- :file:`utils/`: utility functions
- :file:`views/`: contains api endpoints and socketio events
- :file:`db/`: contains database models

.. role:: python(code)
  :language: python
  :class: highlight

To run the application, run :python:`python run.py` from the :file:`app/` directory.

Important files
^^^^^^^^^^^^^^^
:file:`__init__.py`
    - contains the application factory
    - registers blueprints for socketio events and api endpoints
    - loads settings from `.env` file

:file:`.env`
    - contains environment variables for the application

:file:`config.py`
    - contains configuration for authentication, database, and application settings

:file:`agent_storage.py`
    - contains the AgentStorage class
    - used to store and retrieve pre-made agents as they are needed

:file:`chat_queue.py`
    - contains the ChatQueue class
    - when a user sends a message, it is added to the queue to be processed
    - the queue is processed in multiple threads and creates Tasks for each message

:file:`task_manager.py`
    - contains the TaskManager class
    - used to manage the tasks that are created when a message is received
    - tasks are created for each message and are processed in multiple threads
    - tasks creation can be triggered by user messages (top-level tasks), or by Agents (subtasks)

:file:`openai_client.py`
    - contains the OpenAIClient class
    - used to interact with the OpenAI API

STELLA CLI (cli/)
~~~~~~~~~~~~~~~~~
