from flask import Flask, request, render_template, jsonify
from flasgger import Swagger, swag_from
from fingerprint import identify
import json
import os
import pymongo
import pandas as pd
import numpy as np
from sklearn import tree


app = Flask(__name__)
swagger = Swagger(app)

db_connection_url = os.environ['DATABASE_URI']
db_client = pymongo.MongoClient(db_connection_url)
fingerprint_db = db_client.fingerprint


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/user/<user_id>', methods=['DELETE'])
@swag_from('/docs/deleteuser.yml')
def delete_user(user_id):
    return jsonify({
        "wasUserDeleted": True
    })

@app.route('/user/<user_id>', methods=['POST'])
@swag_from('/docs/savepattern.yml')
def save_pattern(user_id):
    keystroke_stream = json.loads(request.data.decode())
    features = identify(keystroke_stream)
    fingerprint_db.features.insert_one({'email':user_id, 'features':features})
    fingerprint_db.keystrokes.insert_one({'email':user_id, 'keystrokes': keystroke_stream})

    return jsonify({
        "wasUserCreated" : True,
        "message": "Created pattern for user " + user_id,
        "fingerprint": features
    })

@app.route('/auth/<user_id>', methods=['POST'])
@swag_from('/docs/verifypattern.yml')
def verify_pattern(user_id):
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
        "confidenceLevel": int(response[0])
    })

if __name__ == '__main__':
    app.run(debug=True)
