import sqlite3
from datetime import datetime, timedelta
from flask import Flask, render_template, request, url_for, flash, redirect, session
from flask_session import Session
from werkzeug.exceptions import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'nosecret'

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)


Session(app)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT id, title, content, created, author FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

def edit_post(post_id):
    conn = get_db_connection()
    post = conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (request.form['title'], request.form['content'], post_id))
    conn.commit()
    conn.close()
    return post

def delete_post(post_id):
    conn = get_db_connection()
    post = conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()
    return post

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    conn = get_db_connection()
    comments = conn.execute('SELECT * FROM comments WHERE post_id = ?', (post_id,)).fetchall()
    conn.close()
    return render_template('post.html', post=post, comments=comments)

@app.route('/create', methods=('GET','POST'))
def create():
    if request.method == 'POST':
        if 'username' not in session:
            return redirect(url_for('login'))
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is needed!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content, author) VALUES (?,?,?)', (title, content, session['name']))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/edit/<int:post_id>', methods=('GET','POST'))
def edit(post_id):
    if request.method == 'POST':
        if 'username' not in session:
            return redirect(url_for('login'))
        title = request.form['title'] 

        if not title:
            flash('Title is needed!')
        else:
            edit_post(post_id)
            return redirect(url_for('post', post_id=post_id))

    return render_template('edit.html', post=get_post(post_id))

@app.route('/<int:post_id>/delete', methods=('POST',))
def delete(post_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    post = get_post(post_id)
    delete_post(post_id)
    flash('"{}" was successfully deleted!'.format(post['title']) )
    return redirect(url_for('index'))


@app.route('/login', methods=('GET','POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username:
            flash('Username is needed!')
        elif not password:
            flash('Password is needed!')
        else:
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
            conn.close()
            if user is None:
                flash('Username does not exist!')
            else:
                if user['password'] != password:
                    flash('Password is incorrect!')
                else:
                    session['username'] = user['username']
                    session['name'] = user['name']
                    session['email'] = user['email']
                    session['member_since'] = user['member_since']
                    return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# register new users
@app.route('/register', methods=('GET','POST'))
def register():
    if request.method == 'GET':
        if session['username'] not in session and session['username'] not in ['admin']:
            flash('Only admin can register new users')
            return redirect(url_for('contactus'))
        
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']
        
        
        if not username:
            flash('Username is needed!')
        elif not name:
            flash('Name is needed!')
        elif not email:
            flash('Email is needed!')
        elif not password:
            flash('Password is needed!')
        elif password != confirm:
            flash('Passwords do not match!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO users (username, name, email, password) VALUES (?,?,?,?)', (username, name, email, password))
            conn.commit()
            conn.close()
            flash('Registration successful')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts WHERE author = ?', (session['name'],)).fetchall()
    conn.close()
    return render_template('profile.html', posts=posts)

# filters for formatting dates
@app.template_filter('iso_to_pretty')
def iso_to_pretty(value, fmt='%B %-d, %Y'):
    return datetime.fromisoformat(value.replace('Z', '+00:00')).strftime(fmt)

@app.route('/contactus', methods=('GET','POST'))
def contactus():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        issue = request.form['issue']
        subject = request.form['subject']
        message = request.form['message']

        if not name:
            flash('Name is needed!')
        elif not email:
            flash('Email is needed!')
        elif not issue:
            flash('Issue is needed!')
        elif not subject:
            flash('Subject is needed!')
        elif not message:
            flash('Message is needed!')
        else:
            flash('Message sent!')
            return redirect(url_for('contactus'))

    return render_template('contactus.html')

@app.route('/add_comment/<int:post_id>', methods=('POST',))
def add_comment(post_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    comment = request.form['comment']
    conn = get_db_connection()
    conn.execute('INSERT INTO comments (post_id, author, content) VALUES (?,?,?)', (post_id, session['name'], comment))
    conn.commit()
    conn.close()
    return redirect(url_for('post', post_id=post_id))

