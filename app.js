var express = require('express');
var app = express();
var http = require('http').createServer(app);
var io = require('socket.io');
io = io.listen(http.listen(process.env.PORT||3000, function(){
  console.log('listening on port '+ process.env.PORT||3000);
}));

io.settings.log = false;
var commandQueue = [];

function parseCommand(msg){
    var command = msg.command.toLowerCase().split(" "); //split the message
    var operator = command[0]; //First word of the command
    switch(msg.operator){
            case "forward":
              io.sockets.emit('hasselhoff', {'message':"forward",'username':msg.username});

              break;
            case "backward":
              io.sockets.emit('hasselhoff', {'message':"backward",'username':msg.username});

              break;
            case "left":
                io.sockets.emit('hasselhoff',{'message':"left",'username':msg.username});
              break;
            case "right":
                  io.sockets.emit('hasselhoff',{'message':"right",'username':msg.username});

              break;
            case "hasselhoff":
                  io.sockets.emit('hasselhoff',{'message':"right",'username':msg.username});
            break;
    }
}


// New call to compress content
//app.use(express.compress());
console.log(__dirname + '/static');
app.use(express.static(__dirname + '/static'));

app.get('/', function(req, res){
  res.sendfile('static/index.html');
});
app.get('/port', function(req, res){
  res.send(process.env.PORT);
});


/*http.listen(process.env.PORT||3000, function(){
  console.log('listening on port '+ process.env.PORT||3000);
});*/

io.sockets.on('connection', function(socket){
    console.log('a user connected');
    io.emit('command',{username:"Server",message:'listening on port '+ process.env.PORT});
    socket.on('command', function(msg){
        parseCommand(msg)
        console.log(msg);
        io.sockets.emit('command', msg);
    });
    socket.on('photo', function(msg){
        console.log("Photo updated");
        io.sockets.emit('photo', msg);
    });
    socket.on('selected', function(msg){
        io.sockets.emit('selected', msg);
    });
});
