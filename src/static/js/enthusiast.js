var score_timeseries = document.getElementById('timeseries');
var data = {
  'size': {
    'height': 300
  },
  'data': {
    'x': 'x',
    'axes': {
      'IMDB Score': 'y2',
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
      'IMDB Score': '#6998A6',
      'gross': '#966001',
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
  'zoom': {}
};
data['axis']['y']['tick']['format'] = d3.format('$.3s')
data['axis']['y2']['tick']['format'] = d3.format('.3s')
data['bindto']='#timeseries-chart'


$('#top').change(function(){update_all()})
$('#language').change(function(){update_all()})
$('#country').change(function(){update_all()})
$('#genre').change(function(){update_all()})
$('#start_year').change(function(){update_all()})
$('#end_year').change(function(){update_all()})

jQuery(document).ready(function(){
  jQuery(".chosen").chosen();
  score_timeseries = c3.generate(data);
  update_all()

});

function update_all(){
  update_words()
  update_ts()
}

function update_ts(){
  var _top = $('#top').val()
  var language = $('#language').val()
  var country = $('#country').val()
  var genre = $('#genre').val()
  var start_year = $('#start_year').val()
  var end_year = $('#end_year').val()

  url = '/api/score_timeseries?'

  if (_top.length>0){url = url + 'top=' + _top + '&'}
  if (language.length>0){url = url + 'language=' + language + '&'}
  if (country.length>0){url = url + 'country=' + country + '&'}
  if (genre.length>0){url = url + 'genre=' + genre + '&'}
  if (start_year.length>0){url = url + 'start_year=' + start_year + '&'}
  if (end_year.length>0){url = url + 'end_year=' + end_year + '&'}

  var updatedData = $.get(url);
  updatedData.done(function(results){
    console.log(updatedData.responseJSON)
    score_timeseries.load(updatedData.responseJSON)
  });

}

function update_words(){
  var _top = $('#top').val()
  var language = $('#language').val()
  var country = $('#country').val()
  var genre = $('#genre').val()
  var start_year = $('#start_year').val()
  var end_year = $('#end_year').val()

  url = '/api/keywords?'

  if (_top.length>0){url = url + 'top=' + _top + '&'}
  if (language.length>0){url = url + 'language=' + language + '&'}
  if (country.length>0){url = url + 'country=' + country + '&'}
  if (genre.length>0){url = url + 'genre=' + genre + '&'}
  if (start_year.length>0){url = url + 'start_year=' + start_year + '&'}
  if (end_year.length>0){url = url + 'end_year=' + end_year + '&'}

  var words = $.get(url)
  words.done(function(data){
    $('#word_cloud').html('')
    $('#word_cloud').jQCloud(words.responseJSON, {
  width: 500,
  height: 350,
  classPattern: null,
  colors: ['#800026', '#bd0026', '#e31a1c', '#fc4e2a', '#fd8d3c', '#feb24c', '#fed976', '#ffeda0', '#ffffcc'],
  fontSize: {
    from: 0.1,
    to: 0.02
  }
});
    
  })
}

