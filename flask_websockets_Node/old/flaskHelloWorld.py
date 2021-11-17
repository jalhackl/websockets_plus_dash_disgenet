from flask import Flask

import socket
import selectors
import types
import testfn as x
sel = selectors.DefaultSelector()

text = "sometext"

app = Flask(__name__)

@app.route('/')
def index():
    b = "something"
    #b = test()
    text = x.calculate_it()
    return text

@app.route('/test')
def run_script():
    import multiServer as ms
    return("starting websockets")

if __name__ == "__main__":
    
    app.run(host='127.0.0.1', port=3001)