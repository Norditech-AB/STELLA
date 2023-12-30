import cmd
import getpass
from cli_design import *
import time
import socketio
import requests
import json
import os
import platform
from cli.command_handler import CommandHandler
import sys

SOCKETIO_NAMESPACE = "/chat"

class Shell(cmd.Cmd):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.waiting_for_response = False
        self.command_handler = CommandHandler(client)

        self.client.connect_to_chat()


        if platform.system() == "Windows":
            os.system('title Stella')
        else:
            sys.stdout.write("\x1b]2;Another Title\x07") #TODO This dont work


    intro = 'Welcome to Stella Shell. Type /help to list commands.\n'
    prompt = '> ' #TODO bug, if you start to write, and delete you can delete this character. This comes from the print, not this line


    def do_login(self, line):
        'Login with username and password'
        args = line.split()
        if len(args) == 0:
            username = input("Username: ")
            password = getpass.getpass("Password: ")
        elif len(args) == 1:
            username = args[0]
            password = getpass.getpass("Password: ")
        else:
            username, password = args[0], args[1]

        self.cli.login(username, password)


    def default(self, line):
        if self.client.waiting_for_response:
            return
        if line.strip() == "":
            return  # Ignore empty inputs
        
        if line.startswith('/'):
            if len(line) == 1:
                print("Unknown command /. Type /help for a list of commands.")
                return
            cmd, arg, line = self.parseline(line[1:])
            arg = arg.split(' ')
            arg = list(filter(None, arg)) #remove empty strings
            cmd_list = [cmd] + arg
            #print with no new line
            self.command_handler(cmd_list)
        else:
            self.client.send_message(line)
        
            

    def do_exit(self, arg):
        print("Goodbye!")
        exit()
    def emptyline(self):
        pass

def print_with_delay(text):
    words = text.split()
    for word in words:
        colored_word = VISS_GREEN + word + ENDC
        print(colored_word, end=" ", flush=False)
        time.sleep(0.04)
    print("\n")  # Move to the next line after the sentence is completed

if __name__ == '__main__':
    Shell().cmdloop()
