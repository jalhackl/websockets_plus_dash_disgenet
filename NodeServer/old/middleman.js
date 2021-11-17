const express = require('express')
const request = require('request');
var bodyParser = require('body-parser');


app = express();
const PORT = 3000;


app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));


// RECEIVE FLASK MSG
app.post("/in", (req, res) => {
  
    // Retrieve array form post body
    var data = req.body;  
    console.log(data);
  
    // Return json response
    //res.json({ result: sum });
});

app.get('/home', function(req, res) {

    request({
        url: 'http://127.0.0.1:5000/flask',
        method: 'POST',
        json: {mes: 'heydude'}
      }, function(error, response, body){
        console.log(body);
      });

/*
    request.post('http://127.0.0.1:5000/flask', function (error, response, body) {
        console.error('error:', error); // Print the error
        console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
        console.log('body:', body); // Print the data received
        res.send(body); //Display the response on the website
      });    
      
      */
});




app.listen(PORT, function (){ 
    console.log('Listening on Port 3000');
}); 

