var express = require('express');
var app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http);

var commandQueue = [];
/*
function parseCommand(msg){
    var command = msg.toLowerCase().split(" "); //split the message
    var operator = command[0]; //First word of the command
    switch(msg):
            case(operator=="move"):
                
} */


// New call to compress content
//app.use(express.compress());
console.log(__dirname + '/static');
app.use(express.static(__dirname + '/static'));

app.get('/', function(req, res){
  res.sendfile('static/index.html');
});
app.get('/port.txt', function(req, res){
  res.sendfile('/port.txt');
});


io.on('connection', function(socket){
    console.log('a user connected');
    io.emit('command',{username:"Server",message:'listening on port '+ process.env.PORT});
    socket.on('command', function(msg){
        commandQueue.push(msg);
        console.log(msg);
        io.emit('command', msg);
    });
});

http.listen(process.env.PORT||3000, function(){
    console.log('listening on port '+ process.env.PORT||3000);
    fs.writeFile('port.txt', process.env.PORT, function(err){
        console.log('File successfully written! - Check your project directory for the output.json file');
    })
});