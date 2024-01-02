import os

import gevent.monkey
gevent.monkey.patch_all()

from app import create_app
import argparse

from dotenv import load_dotenv

load_dotenv()

# Argument parser (Used for CLI)
parser = argparse.ArgumentParser(description='Run STELLA server.')
parser.add_argument('--host', type=str, default=os.getenv('HOST'), help='Host address for the STELLA server')
parser.add_argument('--port', type=int, default=os.getenv('PORT'), help='Host port for the STELLA server')
args = parser.parse_args()

# Create app
app, socketio = create_app(args.host, args.port)

if __name__ == '__main__':
    socketio.run(app, host=args.host, port=args.port, use_reloader=False)
