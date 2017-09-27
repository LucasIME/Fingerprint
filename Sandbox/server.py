from flask import Flask, request, render_template, jsonify
from flasgger import Swagger, swag_from
from fingerprint import identify
import json
import os
import pymongo
import pandas as pd
import numpy as np
from sklearn import tree, metrics
import pickle
from pprint import pprint


app = Flask(__name__)
swagger = Swagger(app)

db_connection_url = os.environ['DATABASE_URI']
db_client = pymongo.MongoClient(db_connection_url)
fingerprint_db = db_client.fingerprint

def to_class(email):
    d = {
        'demeterkoime@gmail.com' : 0,
        'narcelio@outlook.com' : 1,
        'villasv@outlook.com' : 2,
        'meireles31@msn.com' : 3,
        'psmeireles25@gmail.com' : 4, 
        'brunomatissek@hotmail.com' : 5, 
        'pedroplpa@hotmail.com' : 6, 
        'almeida.caio1@gmail.com' : 7,
    }
    return d[email] if email in d else -1

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
    fingerprint_db.email_id.update_one({'email':user_id}, {'$setOnInsert':{'email':user_id}, '$set':{'id':to_class(user_id)}}, upsert=True)

    keystroke_stream = json.loads(request.data.decode())
    features = identify(keystroke_stream)
    fingerprint_db.features.insert_one({'email':user_id, 'features':features})
    fingerprint_db.keystrokes.insert_one({'email':user_id, 'keystrokes':keystroke_stream})

    recalculate_features()
    user_model = create_model_for_id(user_id)
    save_model(user_model, user_id)

    unique_model = create_unique_model()
    save_unique_model(unique_model)

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
    pprint(features)
    target_array = pd.DataFrame.from_dict(features, orient='index').transpose()

    all_users = get_all_users_features_dataframe()

    #clf = load_model_from_user(user_id)
    clf = load_unique_model()

    target_array =  target_array.fillna(all_users.mean())
    target_array = target_array[sorted(target_array.columns)]

    response = clf.predict(target_array)
    print('Response for user {0}: {1}'.format(user_id, response))
    return jsonify({
        "confidenceLevel": int(response == to_class(user_id))
    })

def recalculate_features():
    fingerprint_db.features.remove({})

    for keystroke_obj in fingerprint_db.keystrokes.find():
        keystroke = keystroke_obj['keystrokes']
        cur_user_email = keystroke_obj['email']
        new_features = identify(keystroke)
        fingerprint_db.features.insert_one({'email': cur_user_email, 'features': new_features})
    print("Recalculated features for all users!")

def create_model_for_id(user_id):
    raw_user_features = fingerprint_db.features.find({'email':user_id})
    user_features = pd.DataFrame([user['features'] for user in raw_user_features])

    raw_non_user_features = fingerprint_db.features.find({'email': {'$ne': user_id}})
    non_user_features = pd.DataFrame([user['features'] for user in raw_non_user_features])

    result = pd.concat([user_features, non_user_features]).reset_index(drop=True)
    result = result[sorted(result.columns)]

    X = result.fillna(result.mean())
    Y = [1 for i in range(len(user_features))] + [0 for i in range(len(non_user_features.index))]

    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X, Y)

    print(metrics.confusion_matrix(clf.predict(X), Y))
    print(clf.feature_importances_)
    tree.export_graphviz(clf, out_file=(str(user_id)+'.dot'))

    return clf

def create_unique_model():
    raw_user_features = list(fingerprint_db.features.find({}))
    user_features = pd.DataFrame([user['features'] for user in raw_user_features]).reset_index(drop=True)
    user_features = user_features[sorted(user_features.columns)]
    
    X = user_features.fillna(user_features.mean())
    Y = [to_class(user['email']) for user in raw_user_features]

    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X, Y)

    print('Unique Model Confusion Matrix: ', metrics.confusion_matrix(clf.predict(X), Y))
    print('Unique model feature importance: ', clf.feature_importances_)
    tree.export_graphviz(clf, out_file='uniquemodel.dot')

    return clf

def get_all_users_features_dataframe():
    raw_all_users_features = fingerprint_db.features.find({})
    df = pd.DataFrame([user['features'] for user in raw_all_users_features])
    return df

def save_model(model_obj, user_id):
    binary_model = pickle.dumps(model_obj)
    fingerprint_db.models.update_one({'email': user_id}, {'$setOnInsert':{'email': user_id}, '$set':{'model': binary_model}}, upsert=True)

def save_unique_model(model_obj):
    fingerprint_db.unique_model.remove()
    binary_model = pickle.dumps(model_obj)
    fingerprint_db.unique_model.insert_one({'model': binary_model})

def load_model_from_user(user_id):
    binary_model = fingerprint_db.models.find_one({'email': user_id})
    model = pickle.loads(binary_model['model'])
    return model

def load_unique_model():
    binary_model = fingerprint_db.unique_model.find_one({})
    model = pickle.loads(binary_model['model'])
    return model

def create_all_models():
    for document in fingerprint_db.features.find({}):
        model = create_model_for_id(document['email'])
        save_model(model, document['email'])
    print("Created new models for all users!")
    unique_model = create_unique_model()
    save_unique_model(unique_model)
    print('Create unique model!')

if __name__ == '__main__':
    recalculate_features()
    create_all_models()
    app.run(debug=True)
