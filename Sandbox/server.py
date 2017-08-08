from flask import Flask, request, render_template, jsonify
from flasgger import Swagger
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

@app.route('/colors/<palette>/')
def colors(palette):
    
    all_colors = {
        'cmyk': ['cian', 'magenta', 'yellow', 'black'],
        'rgb': ['red', 'green', 'blue']
    }
    if palette == 'all':
        result = all_colors
    else:
        result = {palette: all_colors.get(palette)}

    return jsonify(result)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/user/<user_id>', methods=['DELETE'])
def deleteUser(user_id):
    #TODO: implement
    return jsonify({
        "message": "User deleted successfully!"
    })

@app.route('/user/<user_id>', methods=['POST'])
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
    """Endpoint to authenticate users
    This is using docstrings for specifications.
    ---
    parameters:
      - name: user_id
        in: path
        type: number
        required: true
        default: 1
      - name: keystroke_array
        in: body
        required: true
        type: array
    definitions:
      Palette:
        type: object
        properties:
          palette_name:
            type: array
            items:
              $ref: '#/definitions/Color'
      Color:
        type: string
    responses:
      200:
        description: A percentage indicating the condifence level
        schema:
          $ref: '#/definitions/Palette'
        examples:
          confidenceLevel: 0.87
    """
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
