from .base_command import BaseCommand
import time
import os
from cli.client.cli_design import *
import sys


class ServeCommand(BaseCommand):
    @staticmethod
    def init_parser(subparsers):
        parser = subparsers.add_parser('serve', help='Start STELLA server')
        parser.add_argument('--host', help='Host to run the server on', default='0.0.0.0')
        parser.add_argument('--port', help='Port to run the server on', default=5001)
        parser.set_defaults(command_class=ServeCommand)

    def execute(self):
        print_info('Starting STELLA server...')
        print_info('Press Ctrl+C to stop the server.')
        print_info('')
        print_info('To continue using the CLI, open a new terminal and run `stella`.')
        time.sleep(2)
        print('')

        current_file_path = os.path.dirname(os.path.abspath(__file__))
        changed_path = os.path.abspath(os.path.join(current_file_path, '../../app'))
        # Change directory to app
        os.chdir(changed_path)

        # Use sys.executable to run the server
        python_interpreter = sys.executable

        # Base command for running the server
        server_command = f'{python_interpreter} run.py --host {self.args.host} --port {self.args.port}'
        os.system(server_command)
