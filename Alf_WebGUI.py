#       Alfred Web Control
#
#       Autor:              Stefan Dimnik
#       Date:               23.10.2020
#       Python:             3.7
#       Projekt Details:    https://github.com/SDim44/Alfred
#       ------------------------------------------------------------
#       
#       V0.1
#       Flask Web Server


from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import math
from multiprocessing import Process, Queue

_debug = False
   
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
CORS(app)
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on_error_default
def default_error_handler(e):
    print("\n\n\t!!!ERROR")
    print(request.event["message"])
    print(request.event["args"])


@socketio.on('control', namespace='/control')
def control(message):
    data = message["data"]

    if "left" in data.keys():
        x = data["left"][0]
        y = data["left"][1]
        if _debug: 
            print("[Server] Left: ",x,",",y)
        #do things with the left joystick
    elif "right" in data.keys():
        x = data["right"][0]
        y = data["right"][1]
        if _debug: 
            print("[Server] Right: ",x,",",y)
        #do things with the right joystick
    elif "A" in data.keys():
        if _debug: 
            print("[Server] A")
        #Button A
    elif "B" in data.keys():
        if _debug: 
            print("[Server] B")
        #Button B

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", debug=True, use_reloader=False)
