from flask import Flask, render_template
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)


@sock.route('/echo')
def echo(ws):
    while True:
        data = ws.receive()
        ws.send(data)


if __name__ == "__main__":
    
    app.run(host='127.0.0.1', port=3000)