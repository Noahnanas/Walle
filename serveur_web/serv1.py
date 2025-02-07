from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/slider', methods=['POST'])
def slider():
    valeur = request.form.get('valeur')
    print(f"Valeur du slider reçue : {valeur}")
    return "Valeur reçue"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
