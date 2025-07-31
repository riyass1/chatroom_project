from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO, emit
import os
import hashlib

app = Flask(__name__)
app.secret_key = 'chatroom_secret_key'
socketio = SocketIO(app)

# تابع هش کردن رمز عبور
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# لود کاربران از فایل
users = {}
if os.path.exists('users.txt'):
    with open('users.txt', 'r') as f:
        for line in f:
            if ':' in line:
                username, password = line.strip().split(':')
                users[username] = password

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed = hash_password(password)

        if username in users and users[username] == hashed:
            session['username'] = username
            return redirect('/chat')
        else:
            error = "نام کاربری یا رمز اشتباه است."

    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed = hash_password(password)

        if username in users:
            message = "این نام کاربری قبلاً ثبت شده است."
        else:
            users[username] = hashed
            with open('users.txt', 'a') as f:
                f.write(f"{username}:{hashed}\n")
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
