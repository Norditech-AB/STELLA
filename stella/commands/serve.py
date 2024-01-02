from .base_command import BaseCommand
import time
import os
from client.cli_design import *


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
        print_info('To continue using the CLI, open a new terminal and run `python cli`.')
        time.sleep(2)
        print('')

        # Change directory to app
        os.chdir('app')

        # Base command for running the server
        server_command = f'python3 run.py --host {self.args.host} --port {self.args.port}'
        os.system(server_command)
