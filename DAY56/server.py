from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import eventlet

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
socketio = SocketIO(app, async_mode='eventlet')

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on('draw_event')
def handle_draw_event(data):
    emit('draw_event', data, broadcast=True, include_self=False)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
