import eventlet
eventlet.monkey_patch()

from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from flask import Flask, render_template, request

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    """Home page."""
    return render_template('index.html')

@socketio.on('connect', namespace='/web')
def connect_web():
    print('[INFO] Web client connected: {}'.format(request.sid))


@socketio.on('disconnect', namespace='/web')
def disconnect_web():
    print('[INFO] Web client disconnected: {}'.format(request.sid))


@socketio.on('connect', namespace='/cv')
def connect_cv():
    print('[INFO] CV client connected: {}'.format(request.sid))


@socketio.on('disconnect', namespace='/cv')
def disconnect_cv():
    print('[INFO] CV client disconnected: {}'.format(request.sid))

@socketio.on('cv2server')
def handle_cv_message(message):
    socketio.emit('server2web', message, namespace='/web')


@socketio.event
def join(message):
    join_room(message['room'])
    emit('server2web',
         {'data': 'In rooms: ' + ', '.join(rooms())})



@socketio.event
def leave(message):
    leave_room(message['room'])
    emit('server2web',
         {'data': 'In rooms: ' + ', '.join(rooms())})

@socketio.event
def my_room_event(message):
    emit('server2web',
         {'data': message['data'],},
         to=message['room'])


def start_server(host='0.0.0.0', port=80):
    print('Starting server http://{}:{}'.format(host, port))
    socketio.run(app=app, host=host, port=port)

if __name__ == "__main__":
    start_server()