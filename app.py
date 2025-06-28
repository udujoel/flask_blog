import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'nosecret'


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
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
    return render_template('post.html', post=post)

@app.route('/create', methods=('GET','POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is needed!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?,?)', (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/edit/<int:post_id>', methods=('GET','POST'))
def edit(post_id):
    if request.method == 'POST':
        title = request.form['title'] 

        if not title:
            flash('Title is needed!')
        else:
            edit_post(post_id)
            return redirect(url_for('post', post_id=post_id))

    return render_template('edit.html', post=get_post(post_id))

@app.route('/<int:post_id>/delete', methods=('POST',))
def delete(post_id):
    post = get_post(post_id)
    delete_post(post_id)
    flash('"{}" was successfully deleted!'.format(post['title']) )
    return redirect(url_for('index'))


@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')
