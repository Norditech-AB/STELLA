Getting Started
===============

Welcome to the Quick Start Guide for STELLA! This guide will help you set up STELLA quickly and efficiently.

Prerequisites
--------------

Before you begin, ensure you have the following:

- Python 3.8 – 3.11 installed.
- Git installed for cloning the repository.
- Basic familiarity with command-line operations.

Step 1: Clone the Repository
----------------------------

Clone the STELLA repository using your preferred method:

**HTTPS:**

.. code-block:: bash

    git clone https://github.com/Norditech-AB/STELLA.git

**SSH:**

.. code-block:: bash

    git clone git@github.com:Norditech-AB/STELLA.git

**GitHub CLI:**

.. code-block:: bash

    gh repo clone Norditech-AB/STELLA


Step 2: Configure the .env File
-------------------------------

Navigate to the STELLA directory and update the `.env` file with your information:

.. code-block:: none

    JWT_SECRET_KEY="<REPLACE ME>"
    BCRYPT_SALT="<REPLACE ME>"
    MONGO_USERNAME="<REPLACE ME>"
    MONGO_PASSWORD="<REPLACE ME>"
    MONGO_URI="<REPLACE ME>"
    MONGO_DB="<REPLACE ME>"
    OPENAI_API_KEY="<REPLACE ME>"
    FLASK_CONFIG="development"
    JWT_ACCESS_TOKEN_EXPIRES="7"
    SOCK_SERVER_OPTIONS_PING_INTERVAL="150"
    ASYNC_MODE="gevent"

Each placeholder should be replaced with your specific values. For instance, `OPENAI_API_KEY` requires a valid API key from OpenAI.

.. tip:: Visit the :doc:`configuration/Environment_Variables` section for detailed guidance on setting up each variable.

.. note:: The `FLASK_CONFIG` variable is set to `development` by default. This is not recommended for production environments.


Step 3: Install Dependencies
-----------------------------

Before running the server, install any necessary dependencies:

.. code-block:: bash

    pip install -r requirements.txt

Step 4: Start the Server
-------------------------

With the environment configured, start the server by running the :file:`run.py` script from the :file:`/app` folder:

.. code-block:: bash

    cd app
    python run.py

.. seealso:: If you encounter issues starting the server, refer to the :doc:`Troubleshooting` guide for common problems and solutions.

Step 5: Explore Default Agents
------------------------------

Explore the default agents provided in :file:`/app/agents/DefaultAgents` to get a feel for STELLA's capabilities.

Step 6: Create Your Workspace
-----------------------------

Create and configure your workspace using the CLI in the :file:`/cli` folder:

1. **Login:**

   .. code-block:: bash

       stella login

2. **Create a Workspace:**

   .. code-block:: bash

       stella workspace create

3. **Add Agents:**

   Add agents to your workspace (replace `<agentid>` with the actual agent ID):

   .. code-block:: bash

       stella add <agentid>

Step 7: Verify the Setup
-------------------------

Verify that STELLA is set up correctly by sending a test message or command. Check for expected responses or outputs to confirm everything is operational.

Next Steps
----------

Congratulations on setting up STELLA! Now, you're ready to dive deeper:

- Learn how to create your first agent in the :doc:`agents/Creating_a_new_Agent` guide.
- Explore advanced CLI commands in the :doc:`cli/index` section.

