const express = require('express');
const app = require('express')();
const server = require('http').createServer(app);
const io = require('socket.io')(server);


// Now attach the socket.io variable with the HTTP server created


// Boolean if armed button has been pressed
var armed = false;

// =========================================
// http web endpoints
// =========================================

app.use(express.static(process.cwd()));

app.get('/', (req,res) => {
  res.sendFile(process.cwd()+"/index.html")
});

app.get('*', function(req, res) {
  res.sendFile(process.cwd()+"/index.html")
})

app.get('/test', (req, res) => {
  //res.set('Content-Type', 'text/html');
  //res.send('Hello World!')
  res.json({ username: 'Flavio' })
});


// =========================================
// Web Namespace
// =========================================
io.of("/web").on('connection', (socket) => {
  console.log('a user connected');
});

// =========================================
// Camera Namespace
// =========================================
io.of("/cam").on('connection', (socket) => {
  console.log('a camera connected');
});


// =========================================
// ROS2 Namespace
// =========================================
io.of("/ros2").on('connection', (socket) => {
  console.log('a user connected in ros2 namespace');

  socket.on('videofeed1', function (msg) {
    io.of("/web").emit('videofeed1', msg);
  });

});

// =========================================
// Drone Namespace
// =========================================
io.of("/control").on('connection', (socket) => {
  console.log('a device entered the control space');

  socket.on('disconnect', function () {
    console.log('user disconnected');
  });

  // SocketIoRos2 bridge
  socket.on('ros2server', function (msg) {
   io.of("/ros2").emit('control', msg);
  });

  // Receive control command
  socket.on('joystick', function (msg) {
    var aux1 = msg[4];

    console.log(msg);

    // Emit commands to consumers
    io.emit('control', msg);
    io.of("/web").emit('control', msg);

    // For arm LED
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

  // Receive data from drone
  socket.on('inferenceresults', function (msg) {
    io.emit('sendNextData', "next");
    io.of("/web").emit('videofeed1', msg);
  });

  // Start video transmission
  socket.on('starttransmission', function (msg) {
    io.emit('sendNextData', "start");
  });

});


// =========================================
// SocketIO endpoints
// =========================================
io.on('connection', function (socket) {

  console.log('user connected');

  socket.on('disconnect', function () {
    console.log('user disconnected');
  });

});





// =========================================
// Start Server
// =========================================
server.listen(5000, () => {
  console.log('listening on *:5000');
});

