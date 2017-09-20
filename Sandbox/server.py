from flask import Flask, request, render_template, jsonify
from flasgger import Swagger, swag_from
from fingerprint import identify
import json
import os
import pymongo
import pandas as pd
import numpy as np
from sklearn import tree
import pickle


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

    recalculate_features()
    user_model = create_model_for_id(user_id)
    save_model(user_model, user_id)
    
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
    target_array = pd.DataFrame.from_dict(features, orient='index').transpose()

    clf = create_model_for_id(user_id)

    target_array =  target_array.fillna(result.mean())
    response = clf.predict(target_array)
    print(response)
    return jsonify({
        "confidenceLevel": int(response[0])
    })

def recalculate_features():
    for keystroke_obj in fingerprint_db.keystrokes.find():
        keystroke = keystroke_obj['keystrokes']
        cur_user_email = keystroke_obj['email']
        new_features = identify(keystroke)
        fingerprint_db.features.update({'email': cur_user_email}, {'email': cur_user_email, 'features': new_features})

def create_model_for_id(user_id):
    raw_user_features = fingerprint_db.features.find_one({'email':user_id})
    user_features = pd.DataFrame.from_dict(raw_user_features['features'], orient='index').transpose()

    raw_non_user_features = fingerprint_db.features.find({'email': {'$ne': user_id}})
    non_user_features = pd.DataFrame([ x['features'] for x in raw_non_user_features])

    result = pd.concat([user_features, non_user_features]).reset_index(drop=True)
    X = result.fillna(result.mean())
    Y = [1] + [0 for i in range(len(non_user_features.index))]
    
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X, Y)

    return clf

def save_model(model_obj, user_id):
    binary_model = pickle.dumps(model_obj)
    fingerprint_db.models.insert_one({'email': user_id, 'model': binary_model})

def load_model_from_user(user_id):
    binary_model = fingerprint_db.models.find_one({'email': user_id})
    model = pickle.loads(binary_model['model'])
    return model

def create_all_models():
    for document in fingerprint_db.features.find({}):
        model = create_model_for_id(document['email'])
        save_model(model, document['email'])

if __name__ == '__main__':
    app.run(debug=True)
