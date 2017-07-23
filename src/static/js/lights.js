$(document).ready(function() {
var top_movementStrength = 50;
var top_width = top_movementStrength / $(window).width();
var top_height = top_movementStrength / $(window).height();
$("#top-image").mousemove(function(e){
          var pageX = e.pageX - ($(window).width() / 2);
          var pageY = e.pageY - ($(window).height() / 2);
          var topX = top_width * pageX * -1 - 25;
          var topY = top_height * pageY * -1 - 50;
          $('#top-image').css("background-position", topX+"px     "+topY+"px");
});

var middle_movementStrength = 15;
var middle_width = middle_movementStrength / $(window).width();
var middle_height = middle_movementStrength / $(window).height();
$("#middle-image").mousemove(function(e){
          var pageX = e.pageX - ($(window).width() / 2);
          var pageY = e.pageY - ($(window).height() / 2);
          var middle_X = middle_width * pageX * -1 - 25;
          var middle_Y = middle_height * pageY * -1 - 50;
          $('#middle-image').css("background-position", middle_X+"px     "+middle_Y+"px");
});

var movementStrength = 5;
var width = movementStrength / $(window).width();
var height = movementStrength / $(window).height();
$("#bottom-image").mousemove(function(e){
          var pageX = e.pageX - ($(window).width() / 2);
          var pageY = e.pageY - ($(window).height() / 2);
          var bottom_X = width * pageX * -1 - 25;
          var bottom_Y = height * pageY * -1 - 50;
          $('#bottom-image').css("background-position", bottom_X+"px     "+bottom_Y+"px");
});



});