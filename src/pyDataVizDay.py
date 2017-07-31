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
import markdown
from textblob import TextBlob

import settings
import etl

from iplotter import C3Plotter
c3 = C3Plotter()

app = Flask(__name__)
api_blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_blueprint, title='pyDataVizday api', 
          default='pyDataVizDay',
          description='This api is used for the pyDataVizDay visualization',
          doc='/doc/',
          version='0.0.1'
          )
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


def return_csv(df, filename='data.csv'):
    try:
        s_buf = io.StringIO()
        df.to_csv(s_buf)
        response = make_response(s_buf.getvalue())
        cd = 'attachment; filename={}.csv'.format(filename)
        response.headers['Content-Disposition'] = cd
        response.mimetype = 'text/csv'
    except AttributeError:
        response = 'AttributeError'
    return response


@app.route('/')
def index():
  body = markdown.markdown(render_template('index.md'), extensions=['markdown.extensions.fenced_code'])
  return render_template('index.html', body=body)

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
    form = render_template('data_form.html', dropdowns=dropdowns, inputs=inputs)
    return render_template('enthusiast.html', form=form)

@app.route('/Exploritory')
def exploritory():
    title = render_template('Exploratory_Charts-Movie_Data-Latest_title.html')
    notebook = render_template('Exploratory_Charts-Movie_Data-Latest.html')
    return render_template('Exploritory.html', body=title + notebook)

@app.route('/slides')
def slides():
    
    slide_body = render_template('slide_body.html')
    return render_template('slides_dark.html', body=slide_body)

@app.route('/slides_light')
def slides_light():
    
    slide_body = render_template('slide_body.html')
    return render_template('slides_light.html', body=slide_body)

def filter_with_args(args):
    try:
      args['genre'] = args['genre'].split(',')
    except:
      pass
    try:
      args['country'] = args['country'].split(',')
    except:
      pass
    try:
      args['language'] = args['language'].split(',')
    except:
      pass

    data_filtered = data.filter(start_year=args['start_year'],
                       end_year=args['end_year'],
                       genre=args['genre'],
                       country=args['country'],
                       language=args['language'],
                       top=args['top']
                       )

    return data_filtered


@api.route('/keywords')
@api.expect(parser)
class keywords(Resource):
  def get(self):
    args = parser.parse_args()
    keyword_data = filter_with_args(args)
    
    c = Counter(keyword_data.keyword.plot_keywords.values.tolist())
    words = [{'text': word[0], 'weight': word[1]} for word in c.most_common(50)]

    return jsonify(words)

@api.route('/top_movies')
@api.expect(parser)
class top_movies(Resource):
  def get(self):
    args = parser.parse_args()
    data = filter_with_args(args)
    
    df = (data.movie
          .sort_values('gross', ascending=False)
          .drop_duplicates(subset=['movie_title'])
          .set_index('movie_title')
          [['title_year', 'imdb_score', 'gross']]
          .head(6)
          )

    return jsonify(df.to_json())

@api.route('/score_timeseries')
@api.expect(parser)
class score_timeseries(Resource):
  def get(self):
    args = parser.parse_args()
    score_data = filter_with_args(args)

    df = (score_data
      .movie
      .sort_values('imdb_score', ascending=False)
     .head(500)
     .groupby(['title_year'])
      .mean()[['imdb_score', 'gross']]
      .rolling(3).mean()
      .dropna()
      .ewm(5).mean()
      .round(3)
      .rename(columns={'imdb_score': 'IMDB Score'})
      )
    df['DATE'] = df.index
    df['DATE'] = df['DATE'].astype('str').fillna('1900-01-01')
    print(df.head())
    score_timeseries = {'columns':[['IMDB Score (right)'] + df['IMDB Score'].values.tolist(),
                                    ['gross'] + df['gross'].values.tolist(),
                                    ['x'] + df.DATE.astype(str).values.tolist()],}
    return jsonify(score_timeseries)

@api.route('/download')
@api.expect(parser)
class download(Resource):
  def get(self):
    args = parser.parse_args()
    data = filter_with_args(args)
    df = data.movie
    return return_csv(df, 'movie.csv')

@api.route('/sentiment')
@api.expect(parser)
class sentiment(Resource):
  def get(self):
    args = parser.parse_args()
    data = filter_with_args(args)
    keywords = TextBlob(' '.join(data.keyword.plot_keywords.values))
    results = {'columns':[['polarity'] + [round(keywords.sentiment.polarity + .1, 3) * 250],
        ['subjectivity'] + [round(keywords.sentiment.subjectivity + .1, 3) * 150]],
        }

    return jsonify(results)


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)