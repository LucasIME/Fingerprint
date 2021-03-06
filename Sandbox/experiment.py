import os
import pymongo
import pandas as pd
import numpy as np
from sklearn import tree, metrics, model_selection
import pickle

db_connection_url = os.environ['DATABASE_URI']
db_client = pymongo.MongoClient(db_connection_url)
experiment_db = db_client.experiment


def main():
    data = pd.read_csv('data.csv')
    data = data.reset_index()
    user_list = get_distinct_users_list(data)
    user_class_list = [int(x) for x in range(len(user_list))]
    user_to_class_map = dict(zip(user_list, user_class_list))

    data = remove_unnecessary_columns(data)
    train_data, test_data = model_selection.train_test_split(data, stratify=data['subject'])
    generate_all_models(train_data, user_list, user_class_list, user_to_class_map)


    total_false_positives = 0
    total_positives = 0
    total_false_negatives = 0
    total_negatives = 0
    for user in user_list:
        user_model = load_model_for_user(user)
        true_Y = test_data['subject'].map(lambda x: 1 if x == user else 0)  
        predicted_Y = user_model.predict(test_data.loc[:, test_data.columns != 'subject'])

        confusion_matrix = metrics.confusion_matrix(true_Y, predicted_Y)
        print(confusion_matrix)
        user_false_positive_rate = confusion_matrix[0][1]/(confusion_matrix[0][1] + confusion_matrix[1][1])
        user_false_negative_rate = confusion_matrix[1][0]/(confusion_matrix[0][0] + confusion_matrix[1][0])
        print('False positive rate for user {0}: {1}'.format(user, user_false_positive_rate))
        print('False negative rate for user {0}: {1}'.format(user, user_false_negative_rate))
        total_positives += confusion_matrix[0][1] + confusion_matrix[1][1]
        total_false_positives += confusion_matrix[0][1]
        total_false_negatives += confusion_matrix[1][0]
        total_negatives += confusion_matrix[0][0] + confusion_matrix[1][0]

    print('Total false positive rate: ', total_false_positives/total_positives)
    print('Total false negative rate: ', total_false_negatives/total_negatives)

def get_distinct_users_list(dataframe):
    return list(dataframe['subject'].unique())

def remove_unnecessary_columns(df):
    df = df.drop('rep', axis=1)
    df = df.drop('sessionIndex', axis=1)
    df = df.drop('index', axis=1)
    return df

def generate_all_models(df, user_list, user_class_list, user_to_class_map):
    for user in user_list:
        user_model = create_model_for_user(df, user, user_to_class_map)
        save_model(user_model, user)
    
def create_model_for_user(df, user_id, user_to_class_map):
    Y = df['subject'].map(lambda x: 1 if x == user_id else 0)  
    X = df.loc[:, df.columns != 'subject']
    
    model = tree.DecisionTreeClassifier(class_weight='balanced')
    model = model.fit(X, Y)

    return model

def save_model(model, user_id):
    binary_model = pickle.dumps(model)
    experiment_db.models.update_one({'id': user_id}, {'$setOnInsert':{'id': user_id}, '$set':{'model': binary_model}}, upsert=True)

def load_model_for_user(user_id):
    binary_model = experiment_db.models.find_one({'id': user_id})
    model = pickle.loads(binary_model['model'])
    return model

main()
