import gevent.monkey
gevent.monkey.patch_all()

from app import create_app
import argparse

# Argument parser (Used for CLI)
parser = argparse.ArgumentParser(description='Run STELLA server.')
parser.add_argument('--host', type=str, default='0.0.0.0', help='Host address for the STELLA server')
parser.add_argument('--port', type=int, default=5001, help='Host port for the STELLA server')
args = parser.parse_args()

# Create app
app, socketio = create_app()

if __name__ == '__main__':
    socketio.run(app, host=args.host, port=args.port, use_reloader=False)
