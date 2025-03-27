from flask_socketio import SocketIO, emit, join_room, leave_room
from laphic_app import create_app  # Import your Flask app factory function

socketio = SocketIO(cors_allowed_origins="*")  # Enable CORS for testing

@socketio.on('connect')
def handle_connect():
    print("A user connected")
    emit('connection_response', {'message': 'Connected to WebSocket'})

@socketio.on('disconnect')
def handle_disconnect():
    print("A user disconnected")

@socketio.on('send_message')
def handle_send_message(data):
    sender = data.get('sender_id')
    receiver = data.get('receiver_id')
    message = data.get('message')
    room = f'room_{sender}_{receiver}'
    emit('receive_message', data, room=room)

@socketio.on('join_room')
def handle_join_room(data):
    room = data.get('room')
    join_room(room)
    emit('room_joined', {'room': room}, room=room)

@socketio.on('leave_room')
def handle_leave_room(data):
    room = data.get('room')
    leave_room(room)
    emit('room_left', {'room': room}, room=room)
