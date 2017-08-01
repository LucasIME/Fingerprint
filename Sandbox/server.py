from flask import Flask, request, render_template, jsonify
from fingerprint import identify
import json
import os
import pymongo


app = Flask(__name__)

db_connection_url = os.environ['DATABASE_URI']
db_client = pymongo.MongoClient(db_connection_url)
fingerprint_db = db_client.fingerprint


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
    keystroke_stream = json.loads(request.data.decode())
    features = identify(keystroke_stream)
    fingerprint_db.features.insert_one({'email':user_id, 'features':features})

    return jsonify({
        "message": "Created pattern for user " + user_id,
        "fingerprint": features
    })

@app.route('/auth/<user_id>', methods=['POST'])
def verifyPattern(user_id):
    #TODO: implement
    return jsonify({
        "message": "User verified successfully!"
    })

if __name__ == '__main__':
    app.run()
