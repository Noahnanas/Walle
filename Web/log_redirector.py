import sys

_socketio = None

def init_socketio(socketio_instance):
    global _socketio
    _socketio = socketio_instance

class WebLogger:
    def write(self, msg):
        if msg.strip() and _socketio:
            _socketio.emit('log_message', msg.strip())
    def flush(self): pass

def redirect_stdout():
    sys.stdout = WebLogger()
    sys.stderr = WebLogger()
