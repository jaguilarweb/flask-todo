from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World Flask again!'

@app.route('/test')
def otro():
    return jsonify({"response": "Flask test"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)