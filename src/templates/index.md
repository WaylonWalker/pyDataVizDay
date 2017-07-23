# pyDataVizDay

*a python implementation of the data viz day visualization*
<div class="col6 center"><br></div>

This site is being used for a capability review of various visualization tools, this one being focused on python.  Python is a general purpose programming language that is very popular for automation, data science, and web development.  This makes python a great choice for data visualization.  It has a very powerful ecosystem for data science that is actively growing.  It has a very stable line of static visualization tools that can output in any image format, as well as a growing number of tools for interacive visualizations in the browser.  Many other languages have similar capabilities in regards to data science, where python is able to stand out against those is when you couple those with its powerful automation and web development capabilities.  Due to this python models are less likely to need rewritten to go to production.


----

## Pages

### [Exploritory](/exploritory)

This page is python's bread and butter in data science today.  It is able to pull in nearly any type of data set imaginable, transorm, aggregate, and plot very quickly.  This page was built using a [jupyter](jupyter.org) notebook.  This a very powerful tool that allows us to do interactive reproducible data science with all of our data, agregations, visualizations, and slides all in one place.


### [Enthusiast](/enthusiast)

With a stong web development ecosystem python is able to serve fully functional, mobile first, web first web apps in production quite quickly after learning a bit of client side languages (html/css/js).  Python is still doing the meat of our data science here, as well as serving up all of the backend.  What python is not very good at is client side scripting.  JavaSript has been the client side scripting language for decades its very powerful, and good at what it does embrace it.  Learning how to attach callbacks to events, get data from forms, fetch data from an api, and update chart is not too difficult to learn.

#### Basic Flask setup

``` python
import markdown
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
  body = markdown.markdown(render_template('index.md'), 
                          extensions=['markdown.extensions.fenced_code'])
  return render_template('index.html', body=body)

if __name__ == '__main__':
    app.run()

```


### [Slides](/slides)

Since we are serving up a web app we can embrace the power and flexibility that this gives us.  The slides for this event will be served along side of the visualization.  This will make these slides available anywhere you have a connection to the web.  These slides were written in markdown, and are very simple to write.
<div class="col6 center"><br></div>
#### Example Markdown Code for Slides
``` markdown

# pyDataVizDay
*a python implementation for Data Viz Day*

![python](https://s3.amazonaws.com/files.dezyre.com/images/blog/Python+for+Data+Science+vs.+Python+for+Web+Development/Python+for+Data+Science+vs+Web+Devlopment.png)

----

# Agenda

1. Viz Walk (3 Views)
    1. Full Web App
    * Simple Web App
    * Exploritory Notebook
* Tools Used
* Other Considerations
* Pros/Cons

```

### [api](/api/doc/#/pyDataVizDay)

The api is required to pass data between the python backend and the front end through a json data structure. This restful api comes with full swagger documentation, follow the link above to play with the api.  The api was created using a flask extension called flask restplus.  This extension used python classes to create each endpoint, and automatically creates the documentation.

#### Example of api endpoint

There is a fair amount of code required here just to get the basic api working.  This can be done much simplier using a plain flask route and jsonify, but you would loose some of the automatic features that flask-restplus provides such as the swagger docs.

``` python
from flask import Flask
from flask import request, render_template, make_response, jsonify, Blueprint, url_for
from flask_restplus import Resource, Api, fields, reqparse
from textblob import TextBlob

import settings
import etl

data = etl.Data()

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

```

----

## Data Source
*[https://www.kaggle.com/deepmatrix/imdb-5000-movie-dataset](https://www.kaggle.com/deepmatrix/imdb-5000-movie-dataset)*

Kaggle provided the imdb-500-movie-dataset for this web app.  It is a small slice of the 3M movies in the imdb dataset.  It was very easy to get started with and provided a few features to that IMDB does not have such as number of faces in the poster.  I found it very difficult to come up with many correlations due to this being such a small dataset and very little data existing for certain categories (countries other than USA, many genres, very few directors/actors repeat)

----

## GitHub
*[https://github.com/WaylonWalker/pyDataVizDay](https://github.com/WaylonWalker/pyDataVizDay)*

All of the code used to create this web app is on github, check it out at the link above.

----

## Leave Your Comments