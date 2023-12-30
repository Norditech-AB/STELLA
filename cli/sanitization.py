import secrets
import bcrypt
import os
import getpass 
from cli_design import *

class Sanitization:
    def __init__(self):
        pass

    def __call__(self, exit_on_fail=True):
        #check project and see if everything is working

        def fail():
            if exit_on_fail: exit(0)
            return False
        
        #check if env is correct
        env_file_path = '../app/.env'

        if not os.path.exists(env_file_path):
            print("Project not configured, try " + VISS_GREEN + "stella config" + ENDC)
            fail()
        
        #check if openai api key is valid
        else:
            print("Project configured")  
            return True
        
        return True

    # Function to read .env file into a dictionary
    def __read_env_file(self,file_path):
        config = {}
        with open(file_path, 'r') as file:
            for line in file:
                if line.strip() and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip().strip('"')
        return config

    # Function to write dictionary back to .env file
    def __write_env_file(self,file_path, config):
        with open(file_path, 'w') as file:
            for key, value in config.items():
                file.write(f'{key}="{value}"\n')

    def __write_template(self,path):
        # Path to your .env file

        #create file if not exist and write default values
        
        #create random 64 char string
        JWT_SECRET_KEY = secrets.token_hex(32) 
        BCRYPT_SALT = bcrypt.gensalt()
        with open(path, 'w') as file:
            file.write(f'JWT_SECRET_KEY="{JWT_SECRET_KEY}"\n')
            file.write(f'JWT_ACCESS_TOKEN_EXPIRES="7"\n')
            file.write(f'SOCK_SERVER_OPTIONS_PING_INTERVAL="150"\n')
            file.write(f'ASYNC_MODE="gevent"\n')
            file.write(f'BCRYPT_SALT="{BCRYPT_SALT}"\n')
            file.write(f'FLASK_CONFIG="development"\n')
            file.write(f'MONGO_USERNAME=""\n')
            file.write(f'MONGO_PASSWORD=""\n')
            file.write(f'MONGO_URI=""\n')
            file.write(f'MONGO_DB="PRODUCTION"\n')
            file.write(f'OPENAI_API_KEY=""\n')
            file.write(f'OVERALL_TASK_MAX_DEPTH="300"\n')
            file.write(f'AGENT_MAX_DEPTH="100"\n')


    def configure_project(self):
        # Path to your .env file
        env_file_path = '../app/.env'

        if not os.path.exists(env_file_path):
            self.__write_template(env_file_path)

        # Read current config
        config = self.__read_env_file(env_file_path)

        #TODO display current value
        # Get user inputs
        config['OPENAI_API_KEY'] = input("Enter your openai api key: ")
        config['MONGO_URI'] = input("Enter your mongo uri: ")
        config['MONGO_USERNAME'] = input("Enter your mongo username: ")
        config['MONGO_PASSWORD'] = getpass.getpass("Enter your mongo password: ")

        # Write updated config back to .env
        self.__write_env_file(env_file_path, config)

        #TODO check if everything checks out 
        print("Project now configured")  
