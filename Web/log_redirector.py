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
        if isinstance(message, str):
            self.terminal.write(message)  # écrit dans le terminal
            self.terminal.flush()
            self.buffer += message
            if '\n' in self.buffer:
                self.terminal.write(f"[WebLogger] Emitting log: {self.buffer.strip()}\n")
                self.terminal.flush()
                _socketio.emit('log_message', self.buffer.strip())
                self.buffer = ""

    def flush(self):
        return self.terminal.flush()

    def isatty(self):
        return self.terminal.isatty()

    def fileno(self):
        return self.terminal.fileno()

def redirect_stdout():
    sys.stdout = WebLogger()
    sys.stderr = WebLogger()
