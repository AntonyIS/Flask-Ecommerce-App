$(document).ready(function(){
  var socket = io.connect('http://127.0.0.1:2000/product/1');

  socket.on('connect', function () {
    socket.send('User has connected!');
  });

  socket.on('message', function (msg) {
    $("#messages").append('<li>'+ msg+ '</li>');
    console.log('Received message');
  })
});