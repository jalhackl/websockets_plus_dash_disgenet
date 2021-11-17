const app = require('express')();
const http = require('http').Server(app);
const io = require('socket.io')(http);
const util = require('util');
const request = require('request');
var bodyParser = require('body-parser');
const port = 3000;
const clients = [];	//track connected clients
//make one reference to event name so it can be easily renamed 
const chatEvent = "chatMessage";

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

// RECEIVE FLASK MSG
app.post("/in", (req, res) => {

    var data = req.body;
    io.emit(chatEvent, data);
    console.log('multicast ' + JSON.stringify(data));
    // Return json response
    //res.json({ result: sum });
});
//Server Web Client
app.get('/', function(req, res){
  res.sendFile(__dirname + '/index.html');
});

//When a client connects, bind each desired event to the client socket
io.on('connection', socket =>{
	//track connected clients via log
	clients.push(socket.id);
	const clientConnectedMsg = 'User connected ' + util.inspect(socket.id) + ', total: ' + clients.length;
	io.emit(chatEvent, clientConnectedMsg);
	console.log(clientConnectedMsg);

	//track disconnected clients via log
	socket.on('disconnect', ()=>{
		clients.pop(socket.id);
		const clientDisconnectedMsg = 'User disconnected ' + util.inspect(socket.id) + ', total: ' + clients.length;
		io.emit(chatEvent, clientDisconnectedMsg);
		console.log(clientDisconnectedMsg);
	})

	//multicast received message from client
	socket.on(chatEvent, msg =>{	
        request({
            url: 'http://127.0.0.1:5000/flask',
            method: 'POST',
            json: {mes : msg , usr :  socket.id}
          }, function(error, response, body){
            
          // console.log(body);
          });

	});
});

//Start the Server
http.listen(port, () => {
  console.log('listening on *:' + port);
});
