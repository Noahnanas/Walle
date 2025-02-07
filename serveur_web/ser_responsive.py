from flask import Flask, render_template, request
from Mvt_walle import Walle

app = Flask(__name__)

# Initialisation de WALL-E
wal = Walle("/dev/ttyACM0")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/servo', methods=['POST'])
def servo():
    servo_id = request.form['servo']
    angle = request.form['angle']

    try:
        angle = float(angle) / 100
        if servo_id in wal.coef:
            wal.manual(servo_id, angle)
            return f"Servo {servo_id} mis à {angle * 100:.0f}%"
        else:
            return f"Erreur : Servo {servo_id} inconnu", 400
    except ValueError:
        return "Erreur : Angle invalide", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
