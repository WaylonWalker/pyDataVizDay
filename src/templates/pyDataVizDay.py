"""
PyDataVizDay

A python implementation of the Data Viz Day visualization built from the Kaggle 
IMDB 5000 Movie Dataset.

"""

from flask import Flask
from flask import request, render_template, make_response, jsonify


app = Flask(__name__):

@app.route('/')
def index():
    return render_template('index.html', body='Hello')




if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='pyDataVizDay')
    parser.add_argument('--port', default='5000')
    parser.add_argument('--debug', dest='debug', action='store_true')
    parser.add_argument('--no_debug', dest='debug', action='store_false')
    parser.set_defaults(debug=False)
    args = parser.parse_args()
    host = socket.gethostbyname(socket.gethostname())
    # webbrowser.open('http://' + str(host) + ':' + str(port) + '/')
    app.run(debug=args.debug, host=str(host), port=int(args.port))