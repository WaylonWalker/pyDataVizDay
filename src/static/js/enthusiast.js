
$('#top').change(function(){update_words()})
$('#language').change(function(){update_words()})
$('#country').change(function(){update_words()})
$('#genre').change(function(){update_words()})
$('#start_year').change(function(){update_words()})
$('#end_year').change(function(){update_words()})

jQuery(document).ready(function(){
  jQuery(".chosen").chosen();
  update_words()

});

function update_words(){
  var _top = $('#top').val()
  var language = $('#language').val()
  var country = $('#country').val()
  var genre = $('#genre').val()
  var start_year = $('#start_year').val()
  var end_year = $('#end_year').val()

  url = 'http://localhost:5000/api/keywords?'

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


