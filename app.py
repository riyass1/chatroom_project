from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
app.secret_key = 'chatroom_secret_key'
socketio = SocketIO(app)

# شبیه پایگاه داده ساده در حافظه
users = {}

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            session['username'] = username
            return redirect('/chat')
        else:
            error = "نام کاربری یا رمز اشتباهه."

    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users:
            message = "این نام کاربری قبلاً ثبت شده."
        else:
            users[username] = password
            message = "ثبت‌نام با موفقیت انجام شد!"

    return render_template('register.html', message=message)

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
