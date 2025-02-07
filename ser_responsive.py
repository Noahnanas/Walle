from flask import Flask, render_template, request
import os
from Mvt_walle import Walle 

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "serveur_web/templates")

app = Flask(__name__, template_folder=TEMPLATE_DIR)

wal = Walle("/dev/ttyACM0")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/servo', methods=['POST'])
def servo():
    servo_id = request.form['servo']
    angle = int(request.form['angle'])
    wal.manual(servo_id, angle)
    return "OK"

@app.route('/blink', methods=['POST'])
def blink():
    wal.blink()
    return "OK"

@app.route('/auto_adjust', methods=['POST'])
def auto_adjust():
    wal.auto_adjust()
    return "OK"

@app.route('/head_angle', methods=['POST'])
def head_angle():
    angle = int(request.form['angle'])
    wal.headAngle(angle)
    return "OK"

@app.route('/sadness', methods=['POST'])
def sadness():
    level = int(request.form['level'])
    wal.sadness(level)
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

