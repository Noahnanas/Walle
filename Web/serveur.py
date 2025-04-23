# web/server.py
from flask import Flask, render_template, Response
from Vision.cam import gen_frames

app = Flask(__name__)
mode_manager = None  # sera injecté plus tard

@app.route('/')
def index():
    active_mode = mode_manager.get_active_mode_name() if mode_manager else "unknown"
    return render_template('indexwebcam.html', mode=active_mode)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def run_web_server(manager_ref):
    global mode_manager
    mode_manager = manager_ref
    app.run(host='0.0.0.0', port=5000)
