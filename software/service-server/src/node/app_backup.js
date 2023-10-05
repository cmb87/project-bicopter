const express = require('express');
const bodyParser = require("body-parser");
const app = require('express')();
const http = require('http').Server(app);
const io = require('socket.io')(http);

// Now attach the socket.io variable with the HTTP server created
io.attach(http, {
 pingInterval: 10000,
 pingTimeout: 5000,
 cookie: false
});

// Boolean if armed button has been pressed
var armed = false;

// =========================================
// http web endpoints
// =========================================
app.use(bodyParser.json());

app.use(express.static(process.cwd()));

app.get('/', (req,res) => {
  res.sendFile(process.cwd()+"/index.html")
});

app.get('*', function(req, res) {
  res.sendFile(process.cwd()+"/index.html")
})

// =========================================
// Web Namespace
// =========================================
io.of("/web").on('connection', (socket) => {
  console.log('a user connected in web namespace');
});

// =========================================
// Camera Namespace
// =========================================
io.of("/cam").on('connection', (socket) => {
  console.log('a user connected in cam1 namespace');
});

// =========================================
// Drone Namespace
// =========================================
io.of("/drone").on('connection', (socket) => {
  console.log('a drone connected');

  socket.on('disconnect', function () {
    console.log('user disconnected');
  });

  // SocketIoRos2 bridge
  socket.on('ros2server', function (msg) {
   console.log(msg);
  });

  // Receive control command
  socket.on('gamepad', function (msg) {
   var aux1 = msg[4];
   var aux2 = msg[5];

   console.log(msg);

   io.emit('control', msg);

   if ( aux1 > 1500 && !armed) {
      console.log("Armed!");
      io.emit('toggleled', "");
      armed = true;

   } else if ( aux1 < 1500 && armed ) {
      console.log("Disarmed!");
      io.emit('toggleled', "");
      armed = false;
   }
  });

  // Toggle led
  socket.on('statechange', function (msg) {
   console.log("statechange: "+msg);
   io.emit('toggleled', "");
  });

});


io.on('connection', function (socket) {









  timeout();
});

function timeout() {
  setTimeout(function () {
   io.emit('state_change_request',"A message from server");
    timeout();
  }, 5000);
}


// =========================================
// SocketIO endpoints
// =========================================
io.on('connection', (socket) => {
  console.log('a user connected');

  socket.on('disconnect', () => {
    console.log('user disconnected');
  });

});

// =========================================
// Start Server
// =========================================
http.listen(5000, () => {
  console.log('listening on *:5000');
});
