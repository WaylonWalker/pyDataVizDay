"""
PyDataVizDay

A python implementation of the Data Viz Day visualization built from the Kaggle 
IMDB 5000 Movie Dataset.

"""

from flask import Flask
from flask import request, render_template, make_response, jsonify


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'

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
    import argparse
    parser = argparse.ArgumentParser(description='pyDataVizDay')
    parser.add_argument('--port', default='5000')
    parser.add_argument('--debug', dest='debug', action='store_true')
    parser.add_argument('--no_debug', dest='debug', action='store_false')
    parser.set_defaults(debug=False)
    args = parser.parse_args()
    # webbrowser.open('http://' + str(host) + ':' + str(port) + '/')
    app.run(debug=args.debug, host='0.0.0.0', port=int(args.port))