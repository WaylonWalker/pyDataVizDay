"""
PyDataVizDay

A python implementation of the Data Viz Day visualization built from the Kaggle 
IMDB 5000 Movie Dataset.

"""

import os
import io
import base64 as b64
from collections import Counter

from flask import Flask
from flask import request, render_template, make_response, jsonify, Blueprint, url_for
from flask_restplus import Resource, Api, fields, reqparse
from flask_cors import CORS, cross_origin
import settings
import etl
import palettes as pal

from iplotter import C3Plotter
c3 = C3Plotter()

app = Flask(__name__)
CORS(app)
api_blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_blueprint, title='pyDataVizday api', 
          description='This api is used for the pyDataVizDay visualization',
          doc='/doc/')
app.register_blueprint(api_blueprint)

parser = reqparse.RequestParser()
parser.add_argument('start_year', help='start date for data', required=False)
parser.add_argument('end_year', help='end date for data', required=False)
parser.add_argument('genre', help='movie genre', required=False)
parser.add_argument('country', help='geographical country location', required=False)
parser.add_argument('language', help='language of the movie (ex. english)', required=False)
parser.add_argument('top', help='top n titles by imdb rating', required=False)
parser.add_argument('title', help='title of the movie', required=False)
parser.add_argument('color', help='"Color" or "Black and White"', required=False)


data = etl.Data()


inputs = ['top', 'start_year', 'end_year']
dropdowns = {'genre': data.genre.genres.dropna().drop_duplicates().values.tolist(),
            'country':data.movie.country.dropna().drop_duplicates().values.tolist(),
            'language':data.movie.language.dropna().drop_duplicates().values.tolist()
            }

@app.route('/')
def index():
    return render_template('index.html', body='Hello')

@app.route('/investor')
def investor():
    form = render_template('data_form.html', dropdowns=dropdowns, inputs=inputs)
    top = 5
    top_countries = (data.movie.groupby('country')
                     .sum()['budget'].sort_values(ascending=False)
                     .head(top).index.values.tolist())
    top_countries_df = (data.movie[data.movie['country'].isin(top_countries)]
                        .groupby(['title_year', 'country']).sum()['budget']
                        .unstack()
                        )

    c3_plot = c3.render(top_countries_df,
                      y_axis_tick_format='s', 
                      title=f'Budget Trend for top {top} countries',
                     colors=pal.todays_outfit)

    return render_template('investor.html', body=form)

@app.route('/enthusiast')
def enthusiast():
    return render_template('enthusiast.html', body='Hello Enthusiast')

@app.route('/slides')
def slides():
    
    slide_body = render_template('slide_body.html', filters=filters)
    return render_template('slides.html', body=slide_body)

@api.route('/keywords')
@api.expect(parser)
class keywords(Resource):
  def get(self):
    args = parser.parse_args()
    keyword_data = data.filter(start_year=args['start_year'],
                               end_year=args['end_year'],
                               genre=args['genre'],
                               country=args['country'],
                               language=args['language'],
                               top=args['top'],
                               title=args['title'],
                               color=args['color']
                               )
    c = Counter(keyword_data.keyword.plot_keywords.values.tolist())
    words = [{'text': word[0], 'weight': word[1]} for word in c.most_common(50)]

    return jsonify(words)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)