#import eventlet
#eventlet.monkey_patch(subprocess=True)

#
import time

import dash
import dash_html_components as html
from flask_socketio import SocketIO

from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc


app = dash.Dash(__name__)

server = app.server
server.debug = False
socketio = SocketIO(server)


app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <script src="//cdnjs.cloudflare.com/ajax/libs/socket.io/2.2.0/socket.io.js" integrity="sha256-yr4fRk/GU1ehYJPAs8P4JlTgu0Hdsp4ZKrx8bDEDC3I=" crossorigin="anonymous"></script>
        
        
        <script src="https://code.jquery.com/jquery-3.5.1.js"></script>
        <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
        
        <script type="text/javascript" charset="utf-8">
            
            var socket = io();
            
            socket.on('connect', function() {
                socket.emit('connected', {data: 'connected'});
            });

            socket.on('shareslider', function(data) {
              
                console.log('data')
                console.log(data)
                //document.getElementById('dummy2').textContent=data;
                document.getElementById('dummy').textContent=data;


                console.log('slider')
                console.log(document.getElementById('slider'))

                dataper = data * 10

                stringel1 = document.getElementById('slider').children[0].children[1].getAttribute("style")
                newsubstringel1 = "width: " + dataper + "%;"
                stringel2 = document.getElementById('slider').children[0].children[3].getAttribute("style")
                newsubstringel2 = "left: " + dataper + "%;"

                replaced1 = stringel1.replace(/width.*;/i, newsubstringel1);

                replaced2 = stringel2.replace(/left.*;/i, newsubstringel2);


                document.getElementById('slider').children[0].children[1].setAttribute("style", replaced1)
                document.getElementById('slider').children[0].children[3].setAttribute("style", replaced2)

            });
            

               

        </script>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

sliderval = 0

app.layout = html.Div([


    dcc.Slider(id='slider', value=sliderval, min=0, max=10, step=1, className='superslider', persistence=True),
    html.Div('value set in javascript:'),
    html.Div(id='dummy'),
    html.Div('value sent to dummy variable in dash callback (optional) == last value chosen on this client:'),
    html.Div(id='dummy2'),
])





@app.callback(
    dash.dependencies.Output('dummy2', 'children'),
    [dash.dependencies.Input('slider', 'value')])
def slidersh(value):
    print("slider value share")

    global sliderval
    sliderval = value

    socketio.emit('shareslider', value)
    
    return value



if __name__ == '__main__':
    #app.run_server(debug=False)
    socketio.run(app.server)