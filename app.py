from flask import Flask, render_template, request, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from database import init_db, get_db
from models import User, Task

app = Flask(__name__)
app.secret_key = 'secret123'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    cur = db.execute('SELECT id, username, password FROM users WHERE id=?', (user_id,))
    row = cur.fetchone()
    return User(*row) if row else None

@app.route('/')
@login_required
def index():
    db = get_db()
    tasks = db.execute('SELECT id, title, completed FROM tasks WHERE user_id=?', (current_user.id,)).fetchall()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form.get('title')
    db = get_db()
    db.execute('INSERT INTO tasks (title, completed, user_id) VALUES (?,0,?)', (title, current_user.id))
    db.commit()
    return redirect('/')

@app.route('/complete/<int:task_id>')
@login_required
def complete(task_id):
    db = get_db()
    db.execute('UPDATE tasks SET completed=1 WHERE id=? AND user_id=?', (task_id, current_user.id))
    db.commit()
    return redirect('/')

@app.route('/delete/<int:task_id>')
@login_required
def delete(task_id):
    db = get_db()
    db.execute('DELETE FROM tasks WHERE id=? AND user_id=?', (task_id, current_user.id))
    db.commit()
    return redirect('/')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        db=get_db()
        row=db.execute('SELECT id, username, password FROM users WHERE username=?',(username,)).fetchone()
        if row and bcrypt.check_password_hash(row[2], password):
            login_user(User(*row))
            return redirect('/')
    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        username=request.form['username']
        password=bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        db=get_db()
        db.execute('INSERT INTO users (username, password) VALUES (?,?)',(username,password))
        db.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

if __name__=='__main__':
    init_db()
    app.run(debug=True)
