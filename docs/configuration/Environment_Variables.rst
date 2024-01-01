Environment Variables
=====================

Environment variables lets you configure STELLA to your specific needs. This guide will walk you through each variable in the :file:`app/.env` file, explaining its purpose and how to set it up.

Overview of `.env` File
------------------------

The :file:`.env` file contains key variables that influence the behavior of your STELLA instance. Here's a look at the standard :file:`.env` file structure:

.. code-block:: none

    JWT_SECRET_KEY="<REPLACE ME>"
    BCRYPT_SALT="<REPLACE ME>"
    ADMIN_KEY="<REPLACE ME>"
    MONGO_USERNAME="<REPLACE ME>"
    MONGO_PASSWORD="<REPLACE ME>"
    MONGO_URI="<REPLACE ME>"
    MONGO_DB="<REPLACE ME>"
    OPENAI_API_KEY="<REPLACE ME>"
    FLASK_CONFIG="development"
    JWT_ACCESS_TOKEN_EXPIRES="7"
    SOCK_SERVER_OPTIONS_PING_INTERVAL="150"
    ASYNC_MODE="gevent"


JWT and Security Keys
----------------------

These keys are essential for securing user authentication and sensitive data within STELLA.

1. **JWT_SECRET_KEY**: Used to encode and decode JWT tokens for user authentication. Generate it securely by running the :file:`setup.py` script in the root folder.

2. **BCRYPT_SALT**: Salt for bcrypt, used in hashing passwords and sensitive information. Also generated via :file:`setup.py`.

3. **ADMIN_KEY**: A special key for accessing admin API endpoints. Use the :file:`setup.py` script to create a secure key.

.. note:: You can run the :file:`setup.py` script by running the following command in the root folder:

    .. code-block:: bash

        python setup.py

MongoDB Atlas Configuration
----------------------------

STELLA uses MongoDB Atlas for its database needs. Follow these steps to configure your MongoDB Atlas variables:

4. **MONGO_USERNAME**: Your MongoDB Atlas username. Create an account on MongoDB Atlas to obtain this.

5. **MONGO_PASSWORD**: Your MongoDB Atlas password.

6. **MONGO_URI**: The URI provided by MongoDB Atlas for your database cluster.

7. **MONGO_DB**: The name of your database within MongoDB Atlas.

Refer to MongoDB Atlas documentation for detailed setup instructions and security best practices.

.. tip:: Follow this `MongoDB Atlas Tutorial <https://www.mongodb.com/basics/mongodb-atlas-tutorial>`_ to quickly get started with MongoDB Atlas.

OpenAI API Configuration
-------------------------

For AI functionalities, STELLA requires an OpenAI API key:

8. **OPENAI_API_KEY**: Register on the OpenAI platform and retrieve your API key from the user dashboard.

.. tip:: You can find your OpenAI API key in your `User Settings on OpenAI <https://platform.openai.com/account/api-keys>`_.

Application Configuration
--------------------------

Configure these variables based on your development or production environment.

9. **FLASK_CONFIG**: Set to `development` for verbose logging during development or `production` for deployment.

10. **JWT_ACCESS_TOKEN_EXPIRES**: Expiration time for JWT access tokens, in days. JWT access tokens are used for user authentication in STELLA.

11. **SOCK_SERVER_OPTIONS_PING_INTERVAL**: Ping interval for the socket server in milliseconds.

12. **ASYNC_MODE**: The mode of asynchronous operation for Flask-SocketIO. Default is `gevent`.


Troubleshooting
---------------

If you encounter any issues with STELLA, please refer to the :doc:`Troubleshooting` guide for solutions to common problems.