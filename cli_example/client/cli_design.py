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


# Usage remains the same


# Usage Example
if __name__ == "__main__":
    spinner = Spinner()
    spinner.start()
    # Simulate a long process
    time.sleep(5)
    spinner.stop()

    spinner.start()
    # Simulate a long process
    time.sleep(5)
    spinner.stop()
