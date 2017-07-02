"""
PyDataVizDay

A python implementation of the Data Viz Day visualization built from the Kaggle 
IMDB 5000 Movie Dataset.

"""

import os
import io
import base64 as b64

from flask import Flask
from flask import request, render_template, make_response, jsonify
import settings
import etl
import palettes as pal

from iplotter import C3Plotter
c3 = C3Plotter()

def fig_to_html(fig):
    """
    converts a matplotlib figure into an html image

    :param fig: matplotlibe figure object
    :returns: STR html string
    """
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    img = ('<img src="data:image/png;base64,{}">'
           .format(b64.b64encode(buf.getvalue()))
           .replace("b'",'')
           .replace("'",''))
    return img

data = etl.Data()
data.load()


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', body='Hello')

@app.route('/investor')
def investor():
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

    return render_template('investor.html', body=c3_plot)

@app.route('/enthusiast')
def enthusiast():
    return render_template('enthusiast.html', body='Hello Enthusiast')

@app.route('/slides')
def slides():
    slide_body = render_template('slide_body.html')
    return render_template('slides.html', body=slide_body)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)