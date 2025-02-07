from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/servo', methods=['POST'])
def servo():
    servo_id = request.form['servo']  # Récupère le servomoteur sélectionné
    angle = request.form['angle']  # Récupère l'angle

    print(f"Servo sélectionné : {servo_id}, Angle : {angle}")  # Affichage côté serveur

    # Ici, tu peux ajouter du code pour contrôler le servomoteur avec GPIO
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
