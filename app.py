from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
app.secret_key = 'chatroom_secret_key'
socketio = SocketIO(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        return redirect('/chat')
    return render_template('login.html')

@app.route('/chat')
def chat():
    username = session.get('username')
    if not username:
        return redirect('/')
    return render_template('chat.html', username=username)

@socketio.on('message')
def handle_message(data):
    emit('message', data, broadcast=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port, allow_unsafe_werkzeug=True)
