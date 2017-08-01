from flask import Flask, request, render_template, jsonify
from fingerprint import identify
import json
import os
import pymongo
import pandas as pd
import numpy as np
from sklearn import tree


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
    fingerprint_db.keystrokes.insert_one({'email':user_id, 'keystrokes': keystroke_stream})

    return jsonify({
        "message": "Created pattern for user " + user_id,
        "fingerprint": features
    })

@app.route('/auth/<user_id>', methods=['POST'])
def verifyPattern(user_id):
    target_keystrokes = json.loads(request.data.decode())
    features = identify(target_keystrokes)
    target_array = [[value for key,value in features.items()]]
    print(target_array)

    user_features = fingerprint_db.features.find_one({'email':user_id})
    non_user_features = list(fingerprint_db.features.find({'email': {'$ne': user_id}}))[:5]
    X = [[ value for key, value in  user_features['features'].items()]] + [ [value for key,value in user['features'].items()] for user in non_user_features]
    Y = [1] + [0 for item in non_user_features]
    print(X)
    print(Y)
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X, Y)
    response = clf.predict(target_array)
    print(response)
    return jsonify({
        "message": "User verified successfully!",
        "response": int(response[0])
    })

if __name__ == '__main__':
    app.run()
