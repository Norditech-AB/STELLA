import sys
import os
import re
import uuid
import subprocess
import bcrypt

def print_banner():
    banner = """
    Starting configuration of STELLA...
      ___ _____ ___ _    _      _   
     / __|_   _| __| |  | |    /_\  
     \__ \ | | | _|| |__| |__ / _ \ 
     |___/ |_| |___|____|____/_/ \_\\
    A Conversational Multi-Agent AI Framework
    
    >>> Visit https://docs.stellaframework.com/ for more information.
    """
    print(banner)

def print_info(message):
    print("\033[1;34m[*]\033[0m " + message)

def print_success(message):
    print("\033[1;32m[+]\033[0m " + message)

def print_error(message):
    print("\033[1;31m[!]\033[0m " + message)

def check_python_version():
    if not (3, 8) <= sys.version_info[:2] <= (3, 11):
        print_error("STELLA requires Python 3.8 to 3.11. Please update your Python version.")
        sys.exit(1)

def backup_env_file(env_path):
    backup_path = env_path + ".backup"
    if not os.path.exists(backup_path):
        with open(env_path, "r") as original, open(backup_path, "w") as backup:
            backup.write(original.read())
        print_success("Backup of .env file created.")

def update_env_file(key, value, env_path):
    if not os.path.exists(env_path):
        print(f"Error: {env_path} does not exist. Please ensure you are in the correct directory.")
        sys.exit(1)

    with open(env_path, "r") as file:
        lines = file.readlines()

    with open(env_path, "w") as file:
        for line in lines:
            if line.startswith(key):
                line = f"{key}=\"{value}\"\n"
            file.write(line)

def setup_database(env_path):
    while True:
        db_choice = input("Choose a database (sqlite/mongodb) [sqlite]: ").strip().lower() or "sqlite"
        if db_choice in ["sqlite", "mongodb"]:
            break
        print_error("Invalid choice. Please enter 'sqlite' or 'mongodb'.")
    
    update_env_file("DATABASE", db_choice, env_path)

    if db_choice == "mongodb":
        mongo_uri = input("Enter your MongoDB URI: ")
        mongo_db_name = input("Enter the MongoDB database name: ")
        update_env_file("MONGO_URI", mongo_uri, env_path)
        update_env_file("MONGO_DB_NAME", mongo_db_name, env_path)

        print_success("MongoDB configured successfully.")
    elif db_choice == "sqlite":
        print_success("SQLite configured successfully.")


def setup_openai_api_key(env_path):
    api_key = input("Enter your OpenAI API key (or leave blank to fill out later): ").strip()
    if api_key:
        update_env_file("OPENAI_API_KEY", api_key, env_path)
        print_success("OpenAI API key configured successfully.")
    else:
        print_info("You can fill out your OpenAI API key later in app/.env.")

def generate_keys(env_path):
    jwt_secret_key = uuid.uuid4().hex
    bcrypt_salt = bcrypt.gensalt().decode("utf-8")
    update_env_file("JWT_SECRET_KEY", jwt_secret_key, env_path)
    update_env_file("BCRYPT_SALT", bcrypt_salt, env_path)

"""
def add_path_to_pythonpath(path):
    if sys.platform.startswith('linux') or sys.platform == 'darwin':
        # For Unix-like systems
        shell_profile = "~/.bashrc" if sys.platform.startswith('linux') else "~/.bash_profile"
        export_line = f'\n# Added by STELLA setup\nexport PYTHONPATH="${{PYTHONPATH}}:{path}"\n'

        with open(os.path.expanduser(shell_profile), "a") as file:
            file.write(export_line)

        print_success(f"Added PYTHONPATH to {shell_profile}. Please restart your terminal or run 'source {shell_profile}'.")

    elif sys.platform == 'win32':
        # For Windows
        import winreg

        with winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER) as hkey:
            with winreg.OpenKey(hkey, r"Environment", 0, winreg.KEY_ALL_ACCESS) as env_key:
                current_pythonpath, _ = winreg.QueryValueEx(env_key, "PYTHONPATH")
                new_pythonpath = f"{current_pythonpath};{path}" if current_pythonpath else path
                winreg.SetValueEx(env_key, "PYTHONPATH", 0, winreg.REG_EXPAND_SZ, new_pythonpath)

        # Inform the user that a logoff/logon might be necessary
        print("Added PYTHONPATH to your system environment variables. You may need to log off and back on for changes to take effect.")

    else:
        print("Unsupported operating system.")
"""


def main():
    print_banner()
    print_info("Initializing STELLA Setup...")
    check_python_version()

    env_path = os.path.join(os.path.dirname(__file__), "app/.env")
    backup_env_file(env_path)
    
    setup_database(env_path)
    setup_openai_api_key(env_path)

    """
    # Ask to modify PYTHONPATH
    cli_path = os.path.dirname(os.path.abspath(__file__))
    add_to_path = input("Do you want to add the STELLA CLI to your PYTHONPATH permanently? [y/N]: ").strip().lower()
    if add_to_path == 'y':
        add_path_to_pythonpath(cli_path)
        print("PYTHONPATH updated successfully.")
    """

    generate_keys(env_path)
    print("")
    print("------------------------------------------------------------")
    print_success(">>> STELLA Setup complete! For more information, visit https://docs.stellaframework.com/")
    print_info("Remember to review and modify other settings in app/.env as needed.")
    print("")
    print("Get started quickly:")
    print("  $ stella serve\t\t\t\t\t# Start STELLA server")
    print("  $ stella register\t\t\t\t\t# Create an account")
    print("  $ stella login\t\t\t\t\t# Login to your account")
    print("  $ stella workspace create\t\t\t# Create a workspace")
    print("  $ stella\t\t\t\t\t\t\t# Start STELLA")
    print("------------------------------------------------------------")


if __name__ == "__main__":
    main()
