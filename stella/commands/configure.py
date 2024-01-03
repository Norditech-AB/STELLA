from .base_command import BaseCommand
import time
import os
from stella.client.cli_design import *
import sys


class ConfigureCommand(BaseCommand):
    @staticmethod
    def init_parser(subparsers):
        parser = subparsers.add_parser('configure', help='Configure STELLA.')
        parser.set_defaults(command_class=ConfigureCommand)

    def execute(self):
        current_file_path = os.path.dirname(os.path.abspath(__file__))
        stella_path = os.path.abspath(os.path.join(current_file_path, '../../'))

        # Change directory to app
        os.chdir(stella_path)

        # Use sys.executable to run the server
        python_interpreter = sys.executable

        # Base command for running the server
        server_command = f'{python_interpreter} {stella_path}/configure.py'
        os.system(server_command)
