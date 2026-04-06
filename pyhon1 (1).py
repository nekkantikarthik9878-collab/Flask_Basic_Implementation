from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)

def load_users():
    users = {}
    try:
        with open('users.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if ':' in line:
                    username, password = line.split(':', 1)
                    users[username] = password
    except FileNotFoundError:
        pass
    return users

def save_user(username, password):
    with open('users.txt', 'a') as f:
        f.write(f"{username}:{password}\n")

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    msg_type = ''
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        users = load_users()
        if username in users and users[username] == password:
            message = f"Welcome back, {username}! You are logged in 🎉"
            msg_type = 'success'
        elif username not in users:
            message = "Username not found. Please register first!"
            msg_type = 'error'
        else:
            message = "Wrong password. Please try again!"
            msg_type = 'error'
    return render_template('login.html', message=message, msg_type=msg_type)

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    msg_type = ''
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        if not username or not password:
            message = "Please fill in both fields!"
            msg_type = 'error'
        else:
            users = load_users()
            if username in users:
                message = "That username is already taken. Try another!"
                msg_type = 'error'
            else:
                save_user(username, password)
                message = f"Account created for '{username}'! Go login now 🚀"
                msg_type = 'success'
    return render_template('register.html', message=message, msg_type=msg_type)

if __name__ == '__main__':
    app.run(debug=True)