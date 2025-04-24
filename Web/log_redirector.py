import sys

_socketio = None

def init_socketio(socketio_instance):
    global _socketio
    _socketio = socketio_instance

class WebLogger:
    def __init__(self):
        self.terminal = sys.__stdout__  # garde accès au terminal
        self.buffer = ""

    def write(self, message):
        self.terminal.write(message)  # écrit dans le terminal
        self.terminal.flush()
        self.buffer += message
        if '\n' in self.buffer:
            from server import socketio  # importe à l’intérieur
            socketio.emit('log_message', self.buffer.strip())
            self.buffer = ""

    def flush(self):
        pass

def redirect_stdout():
    sys.stdout = WebLogger()
    sys.stderr = WebLogger()
