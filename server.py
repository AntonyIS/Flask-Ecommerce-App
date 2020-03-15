from app import app
from app import socketio,send


@socketio.on("message")
def handleMessage(msg):
    print("Message: " + msg)
    send(msg,broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True)

