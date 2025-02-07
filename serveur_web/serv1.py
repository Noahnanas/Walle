from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/servo', methods=['POST'])
def servo():
    servo_id = request.form['servo']  # Récupère le servomoteur sélectionné
    angle = request.form['angle']  # Récupère l'angle envoyé par le client

    print(f"Servo sélectionné : {servo_id}, Angle : {angle}°")  # Affichage côté serveur

    # Ici, ajoute ton code pour contrôler les servos avec le Raspberry Pi
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

