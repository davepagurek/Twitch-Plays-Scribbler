var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);

var commandQueue = [];

function isValidCommand(msg){
    var command = msg.toLowerCase().split(" "); //split the message
    var operator = command[0]; //First word of the command
    switch(msg):
            case(operator=="move")
}

app.get('/', function(req, res){
  res.sendfile('/templates/index.html');
});

io.on('connection', function(socket){
    console.log('a user connected');
    socket.on('command', function(msg){
        commandQueue.push(msg);
        io.emit('command', msg);
    });
});

http.listen(process.env.PORT||3000, function(){
  console.log('listening on port '+ process.env.PORT||3000);
});