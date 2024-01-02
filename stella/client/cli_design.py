import json
import threading
import itertools
import time
import sys

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'

ENDC = '\033[0m'  #default
VISS_GREEN = '\033[38;5;43m'

BOLD = '\033[1m'
UNDERLINE = '\033[4m'
DIM = '\033[2m'
ITALIC = '\033[3m' #(not widely supported)
BLINK = '\033[5m' #(not widely supported, and generally discouraged)


def print_info(message):
    print(BLUE + "[*]\033[0m " + message)


def print_success(message):
    print(GREEN + "[+]\033[0m " + message)


def print_error(message):
    print(RED + "[!]\033[0m " + message)


def print_banner():
    banner = """
      ___ _____ ___ _    _      _   
     / __|_   _| __| |  | |    /_\  
     \__ \ | | | _|| |__| |__ / _ \ 
     |___/ |_| |___|____|____/_/ \_\\
    """
    print(banner)


def pretty_print_workspaces(workspaces):
    # If the length of the workspaces list is 0, print a message and return
    if len(workspaces) == 0:
        print_info("You have no workspaces. Type /workspace create <name> to create one.")
        return

    # Calculate the maximum length of the ID as a string
    id_length = max(max(len(str(workspace['id'])) for workspace in workspaces), 2)

    # Define a maximum name length
    max_name_length = 15

    print_info("Workspaces:")
    # Create the header with dynamic spacing
    header = f" | {'ID':>{id_length}} | {'Name':<{max_name_length}} | {'Number of Agents':^16} |"
    print(header)

    for workspace in workspaces:
        # Truncate the name if it's longer than the max length
        name = workspace['name']
        if len(name) > max_name_length:
            name = name[:max_name_length - 3] + '...'

        # Use dynamic width for ID based on the longest ID
        print(f" | {workspace['id']:>{id_length}} | {name:<{max_name_length}} | {len(workspace['agents']):^16} |")
    print_info("To switch workspace, type /workspace switch <id>")


def pretty_print_workspace(workspace):
    agents = workspace.get('agents', {})
    print_info("Workspace info:")
    print(f" Name: {workspace['name']}")
    print(f" ID: {workspace['id']}")
    print(f" Number of agents: {len(workspace['agents'])}")
    print(f" Agents:")
    for agent_id, agent in agents.items():
        print(f"  - {agent_id}")


class Spinner:
    def __init__(self, message="", delay=0.1):
        self.message = message
        self.delay = delay
        # Spinner characters to create a spinning effect
        self.spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.stop_running = threading.Event()
        self.thread = None

    def spin(self):
        for char in itertools.cycle(self.spinner_chars):
            if self.stop_running.is_set():
                break
            sys.stdout.write(f"\r{self.message} {char}")
            sys.stdout.flush()
            time.sleep(self.delay)

        sys.stdout.write('\r' + '' * (len(self.message) + 2) + '\r')  # Clear line

    def start(self):
        if self.thread and self.thread.is_alive():
            self.stop_running.set()
            self.thread.join()

        self.stop_running.clear()
        self.thread = threading.Thread(target=self.spin)
        self.thread.start()

    def stop(self):
        self.stop_running.set()
        if self.thread:
            self.thread.join()
