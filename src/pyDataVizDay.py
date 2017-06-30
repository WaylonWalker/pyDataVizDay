"""
PyDataVizDay

A python implementation of the Data Viz Day visualization built from the Kaggle 
IMDB 5000 Movie Dataset.

"""

import os
from flask import Flask
from flask import request, render_template, make_response, jsonify


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', body='Hello')

@app.route('/investor')
def investor():
    return render_template('investor.html', body='Hello Investor')

@app.route('/enthusiast')
def enthusiast():
    return render_template('enthusiast.html', body='Hello Enthusiast')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)