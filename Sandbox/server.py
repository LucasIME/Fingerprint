from flask import Flask, request, render_template, jsonify
from fingerprint import identify
import json


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/fingerprint', methods=['POST'])
def fingerprint():
    keystroke_stream = json.loads(request.data.decode())
    return jsonify({
        "fingerprint": identify(keystroke_stream)
    })

@app.route('/user/<user_id>', methods=['GET'])
def checkUser(user_id):
    #TODO: implement
    return jsonify({
        "message": "User exists!"
    })

@app.route('/user/<user_id>', methods=['DELETE'])
def deleteUser(user_id):
    #TODO: implement
    return jsonify({
        "message": "User deleted successfully!"
    })

@app.route('/save/<user_id>', methods=['POST'])
def savePattern(user_id):
    #TODO: implement
    return jsonify({
        "message": "Created pattern for user " + user_id
    })

@app.route('/auth/<user_id>', methods=['POST'])
def verifyPattern(user_id):
    #TODO: implement
    return jsonify({
        "message": "User verified successfully!"
    })

if __name__ == '__main__':
    app.run()
