from flask import Flask, request, render_template, jsonify
from fingerprint import identify
import json


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/fingerprint', methods=['POST'])
def fingerprint():
    keystroke_stream = json.loads(request.data)
    return jsonify({
        "fingerprint": identify(keystroke_stream)
    })

if __name__ == '__main__':
    app.run()
