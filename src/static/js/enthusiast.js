var score_timeseries = document.getElementById('timeseries');
var mil = d3.format('$.3s')
var update_freq = 200


// $(document).ready(function() {
var style = getComputedStyle(document.body);
score_color = style.getPropertyValue('--score-color');
gross_color = style.getPropertyValue('--gross-color');

score_color = '#0C243B';
gross_color = '#4D9913';
// }


var data = {
  'size': {
    'height': 300
  },
  'data': {
    'x': 'x',
    'axes': {
      'IMDB Score (right)': 'y2',
      'gross': 'y',
      'x': 'y'
    },
    'columns': [
    [
    'IMDB Score'
    ],
    [
    'gross'
    ],
    [
    'x'
    ]
    ],
    'colors': {
      'IMDB Score (right)': score_color,
      'gross': gross_color,
      'x': '#08414C'
    }
  },
  'subchart': {
    'show': false
  },
  'point': {
    'show': false
  },
  'grid': {
    'x': {
      'show': false
    },
    'y': {
      'show': false
    }
  },
  'axis': {
    'rotated': false,
    'x': {
      'type': 'timeseries',
      'tick': {
        'count': 10,
        'values': false,
        'culling': {},
        'format': '%Y-%m-%d'
      }
    },
    'y': {
      'tick': {
        'format': ''
      }
    },
    'y2': {
      'tick': {},
      'show': true
    }
  },
  'zoom': {'enabled': true},
  'tooltip': {
    'contents': function (data)
    {
        var date = Date(data[0]['x'])
        var year = data[0]['x'].getYear()+1900
        var score = data[0].value
        var gross = mil(data[1].value)
        $('#year').html(year)
        $('#score').html(score)
        $('#gross').html(gross)
        $('#top-movies-year').html(' for ' + year)
        if ((performance.now() - window.last_update)>update_freq)
        {
            window.last_update = performance.now()
            var year = data[0]['x'].getYear()+1900
            update_words_year(year)
            update_sentiment_year(year)
            update_top_movies(String(parseInt(year) - 1), String(parseInt(year) + 1))
            }
    }
  }
};

data['axis']['y']['tick']['format'] = d3.format('$.3s')
data['axis']['y2']['tick']['format'] = d3.format('.3s')
data['bindto']='#timeseries-chart'

var sentiment_data = {
    bindto:'#sentiment-chart',
    data: {
        colors: {
          polarity: "#000016",//chroma(score_color).darken().hex(),
          subjectivity: score_color, },
        columns: [
            ['polarity', 10],
            ['subjectivity', 10],
        ],
        type: 'bar',

    },
    bar: {
        width: {
            ratio: 100 // this makes bar width 50% of length between ticks
        },
        // or
        // width: 100 // this makes bar width 100px
    },
    axis:{rotated:true,
        y:{min:0, max:100, show:false},
        x:{labels:'', show:false}
    },
    tooltip:{show:false},
    grid: {y: {lines: [{value:10, text:'neutral'},
                       {value:100, text:'positive'},
                       {value:100, text:'     subjective', position:'start'},
                       {value:0, text:'negative'},
                       {value:0, text:'     objective', position:'start'},
                       ]}}

}


function update_word_cloud_settings(){

console.log('update')
if (window.innerWidth > 1000){
    wc_width = 500
    wc_height = 350    
}
else {
    wc_width = 300
    wc_height = 350
}


word_coud_settings =     {
      width: wc_width,
      height: wc_height,
      classPattern: null,
      colors: [score_color, 
               // chroma(score_color).darken().hex(), 
               "#000016",
               // chroma(score_color).darken().darken().hex(), 
               "#000000",
               ],
      fontSize: {
        from: 0.1,
        to: 0.02
        }
    }
  
  return word_coud_settings;
}



var _top = $('#top')
var language = $('#language')
var country = $('#country')
var genre = $('#genre')
var start_year = $('#start_year')
var end_year = $('#end_year')


$('#top').change(function(){update_all()})
$('#language').change(function(){update_all()})
$('#country').change(function(){update_all()})
$('#genre').change(function(){update_all()})
$('#start_year').change(function(){update_all()})
$('#end_year').change(function(){update_all()})
$('#download').click(function(){download()})

jQuery(document).ready(function(){
  jQuery(".chosen").chosen();
  score_timeseries = c3.generate(data);
  sentiment_chart = c3.generate(sentiment_data)
  $('#word_cloud').jQCloud([{'text':'pyDataVizDay', 'weight':1}], update_word_cloud_settings())
  update_all()


});

function download(){
    url = url_params('/api/download?')
    window.location = url
}
function update_all(){
  update_words()
  update_ts()
  update_sentiment()
  update_top_movies()
  last_update = performance.now()
}

function url_params(base, start_year_val, end_year_val)
{

    // start_year = typeof start_year_val !== 'undefined' ? start_year.val()
    var start_year_val = typeof start_year_val !== 'undefined' ? start_year_val: start_year.val() 
    var end_year_val = typeof end_year_val !== 'undefined' ? end_year_val: end_year.val()

    var url = base
    if (_top.val().length>0){url = url + 'top=' + _top.val() + '&'}
    if (language.val().length>0){url = url + 'language=' + language.val() + '&'}
    if (country.val().length>0){url = url + 'country=' + country.val() + '&'}
    if (genre.val().length>0){url = url + 'genre=' + genre.val() + '&'}
    if (start_year_val>0){url = url + 'start_year=' + String(start_year_val) + '&'}
    if (end_year_val>0){url = url + 'end_year=' + String(end_year_val) + '&'}
    
    return url
}

function update_ts()
{
  score_timeseries.flow({'done': load_ts()})

}

function load_ts()
{
  url = url_params('/api/score_timeseries?')
  var updatedData = $.get(url);
  updatedData.done(function(results)
  {
    score_timeseries.load(updatedData.responseJSON)
  })
}

function update_sentiment()
{
  sentiment_chart.flow({'done': load_sentiment()})

}
function load_sentiment()
{
  url = url_params('/api/sentiment?')
  var updatedData = $.get(url);
  updatedData.done(function(results)
  {
    sentiment_chart.load(updatedData.responseJSON)
  })
    
}

function update_words()
{
  url = url_params('/api/keywords?')

  var words = $.get(url)
  words.done(function(data)
  {
    $('#word_cloud').jQCloud('update', words.responseJSON)
  })
}


function update_top_movies(start_year, end_year)
{
    var url = url_params('/api/top_movies?', start_year, end_year)

    var top_movies = $.get(url)
    var promises = []
    top_movies.done(function()
    {
        tm = JSON.parse(top_movies.responseJSON)
        h = ''
        for (title in tm['gross']) {
            // console.log(title)
            var info = $.get('http://www.omdbapi.com/?t=' + title + '&apikey=90424a9e')
            promises.push(info)
        }
        $.when.apply(null, promises).done(function(){
            // console.log(promises)
            window.promises = promises
        for (i in promises){
            console.log()
            $('#poster-' + i).html('<img src=' + promises[i].responseJSON['Poster'] + ' width=75%>')
            $('#title-' + i).html(promises[i].responseJSON['Title'])

        }
            // $('#top_movies').html(h)
            // console.log(h)
})
        // console.log(poster(title))
    }

                    )
}



function update_words_year(year)
{

    var url = '/api/keywords?start_year=' + String(parseInt(year) - 1) + '&end_year=' + String(parseInt(year) + 1) + '&'
    if (_top.val().length>0){url = url + 'top=' + _top.val() + '&'}
    if (language.val().length>0){url = url + 'language=' + language.val() + '&'}
    if (country.val().length>0){url = url + 'country=' + country.val() + '&'}
    if (genre.val().length>0){url = url + 'genre=' + genre.val() + '&'}

  var words = $.get(url)
  words.done(function(data)
  {
    // $('#word_cloud').html('')
    $('#word_cloud').jQCloud('update', words.responseJSON, update_word_cloud_settings());
    
  })
}

function update_sentiment_year(year)
{

    var url = '/api/sentiment?start_year=' + String(parseInt(year) - 1) + '&end_year=' + String(parseInt(year) + 1) + '&'
    if (_top.val().length>0){url = url + 'top=' + _top.val() + '&'}
    if (language.val().length>0){url = url + 'language=' + language.val() + '&'}
    if (country.val().length>0){url = url + 'country=' + country.val() + '&'}
    if (genre.val().length>0){url = url + 'genre=' + genre.val() + '&'}

  var updatedData = $.get(url);
  updatedData.done(function(results)
  {
    sentiment_chart.load(updatedData.responseJSON)
  })

}

$(window).resize(function(){
  var settings = update_word_cloud_settings()
  console.log(settings)
  $('#word_cloud').empty();
  $('#word_cloud').jQCloud('destroy')
  $('#word_cloud').jQCloud([{'text':'pyDataVizDay', 'weight':1}], settings)
  update_words()
})