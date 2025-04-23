from flask import Flask, render_template, Response, request, redirect
from Vision.cam import gen_frames
import threading

app = Flask(__name__)
selected_mode = "Manual"  # valeur par défaut

@app.route('/')
def index():
    return render_template('indexwebcam.html', mode=selected_mode)

@app.route('/set_mode', methods=["POST"])
def set_mode():
    global selected_mode
    selected_mode = request.form.get("mode")
    print(f"Mode received from web: {selected_mode}")
    return redirect('/')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def get_selected_mode():
    return selected_mode

def run_web_server():
    app.run(host='0.0.0.0', port=5000)
