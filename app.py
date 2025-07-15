import sqlite3
import os
from datetime import datetime, timedelta
from flask import Flask, render_template, request, url_for, flash, redirect, session, Blueprint
from flask_session import Session
from werkzeug.exceptions import abort

# Initialize Flask app and configure session
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'nosecret')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
Session(app)

# Blueprint for all forum/blog routes, with URL prefix
forum_bp = Blueprint('forum_bp', __name__)

def get_db():
    if os.environ.get('DATABASE_URL'):
        import psycopg2
        from psycopg2.extras import RealDictCursor
        conn = psycopg2.connect(os.environ['DATABASE_URL'], cursor_factory=RealDictCursor)
        cur = conn.cursor()
        return conn, cur
    else:
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        return conn, conn

def get_post(post_id):
    conn, cur = get_db()
    if os.environ.get('DATABASE_URL'):
        cur.execute('SELECT * FROM posts WHERE id = %s', (post_id,))
        post = cur.fetchone()
    else:
        cur.execute('SELECT * FROM posts WHERE id = ?', (post_id,))
        post = cur.fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

def edit_post(post_id):
    conn, cur = get_db()
    if os.environ.get('DATABASE_URL'):
        cur.execute('UPDATE posts SET title = %s, content = %s WHERE id = %s', (request.form['title'], request.form['content'], post_id))
    else:
        cur.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (request.form['title'], request.form['content'], post_id))
    conn.commit()
    conn.close()

    return None

def delete_post(post_id):
    conn, cur = get_db()
    if os.environ.get('DATABASE_URL'):
        cur.execute('DELETE FROM posts WHERE id = %s', (post_id,))
    else:
        cur.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()
    return None

@forum_bp.route('/')
def index():
    """Home page: show all blog posts."""
    conn, cur = get_db()
    if os.environ.get('DATABASE_URL'):
        cur.execute('SELECT id, title, content, created, author FROM posts')
        posts = cur.fetchall()
    else:
        cur.execute('SELECT id, title, content, created, author FROM posts')
        posts = cur.fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@forum_bp.route('/<int:post_id>')
def post(post_id):
    """View a single post and its comments. Allows adding comments if logged in."""
    post = get_post(post_id)
    conn, cur = get_db()
    if os.environ.get('DATABASE_URL'):
        cur.execute('SELECT * FROM comments WHERE post_id = %s', (post_id,))
        comments = cur.fetchall()
    else:
        cur.execute('SELECT * FROM comments WHERE post_id = ?', (post_id,))
        comments = cur.fetchall()
    conn.close()
    return render_template('post.html', post=post, comments=comments)

@forum_bp.route('/create', methods=('GET','POST'))
def create():
    """Create a new blog post. Only for logged-in users."""
    if request.method == 'POST':
        if 'username' not in session:
            return redirect(url_for('forum_bp.login'))
        title = request.form['title']
        content = request.form['content']
        conn, cur = get_db()
        if not title:
            flash('Title is needed!')
        else:
            if os.environ.get('DATABASE_URL'):
                cur.execute('INSERT INTO posts (title, content, author) VALUES (%s, %s, %s)', (title, content, session['name']))
            else:
                cur.execute('INSERT INTO posts (title, content, author) VALUES (?, ?, ?)', (title, content, session['name']))
            conn.commit()
            conn.close()
            return redirect(url_for('forum_bp.index'))
    return render_template('create.html')

@forum_bp.route('/edit/<int:post_id>', methods=('GET','POST'))
def edit(post_id):
    """Edit a post. Only the post creator can edit."""
    if request.method == 'POST':
        if 'username' not in session:
            return redirect(url_for('forum_bp.login'))
        title = request.form['title']
        if not title:
            flash('Title is needed!')
        else:
            edit_post(post_id)
            return redirect(url_for('forum_bp.post', post_id=post_id))
    return render_template('edit.html', post=get_post(post_id))

@forum_bp.route('/<int:post_id>/delete', methods=('POST',))
def delete(post_id):
    """Delete a post. Only the post creator can delete."""
    if 'username' not in session:
        return redirect(url_for('forum_bp.login'))
    post = get_post(post_id)
    delete_post(post_id)
    flash('"{}" was successfully deleted!'.format(post['title']) )
    return redirect(url_for('forum_bp.index'))

@forum_bp.route('/login', methods=('GET','POST'))
def login():
    """User login. Sets session variables on success."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username:
            flash('Username is needed!')
        elif not password:
            flash('Password is needed!')
        else:
            conn, cur = get_db()
            if os.environ.get('DATABASE_URL'):
                cur.execute('SELECT * FROM users WHERE username = %s', (username,))
                user = cur.fetchone()
            else:
                cur.execute('SELECT * FROM users WHERE username = ?', (username,))
                user = cur.fetchone()
            conn.close()
            if user is None:
                flash('Username does not exist!')
            else:
                if user['password'] != password:
                    flash('Password is incorrect!')
                else:
                    # Store user info in session
                    session['username'] = user['username']
                    session['name'] = user['name']
                    session['email'] = user['email']
                    session['member_since'] = user['member_since']
                    return redirect(url_for('forum_bp.index'))
    return render_template('login.html')

@forum_bp.route('/logout')
def logout():
    """Log out the current user."""
    session.pop('username', None)
    return redirect(url_for('forum_bp.index'))

@forum_bp.route('/register', methods=('GET','POST'))
def register():
    """Register a new user. Only admin can register new users."""
    if request.method == 'GET':
        if session.get('username') not in session and session.get('username') not in ['admin']:
            flash('Only admin can register new users')
            return redirect(url_for('forum_bp.contactus'))
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
            conn, cur = get_db()
            if os.environ.get('DATABASE_URL'):
                cur.execute('INSERT INTO users (username, name, email, password) VALUES (%s, %s, %s, %s)', (username, name, email, password))
            else:
                cur.execute('INSERT INTO users (username, name, email, password) VALUES (?, ?, ?, ?)', (username, name, email, password))
            conn.commit()
            conn.close()
            flash('Registration successful')
            return redirect(url_for('forum_bp.login'))
    return render_template('register.html')

@forum_bp.route('/profile')
def profile():
    """Show the profile page for the logged-in user, including their posts."""
    if 'username' not in session:
        return redirect(url_for('forum_bp.login'))
    conn, cur = get_db()
    if os.environ.get('DATABASE_URL'):
        cur.execute('SELECT * FROM posts WHERE author = %s', (session['name'],))
        posts = cur.fetchall()
    else:
        cur.execute('SELECT * FROM posts WHERE author = ?', (session['name'],))
        posts = cur.fetchall()
    conn.close()
    return render_template('profile.html', posts=posts)

@app.template_filter('iso_to_pretty')
def iso_to_pretty(value, fmt='%B %-d, %Y'):
    if isinstance(value, datetime):
        return value.strftime(fmt)
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace('Z', '+00:00')).strftime(fmt)
        except Exception:
            return value  # fallback: return as-is
    return str(value)

@forum_bp.route('/contactus', methods=('GET','POST'))
def contactus():
    """Contact us form. Handles user messages to the admin/support."""
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
            return redirect(url_for('forum_bp.contactus'))
    return render_template('contactus.html')

@forum_bp.route('/add_comment/<int:post_id>', methods=('POST',))
def add_comment(post_id):
    """Add a comment to a post. Only for logged-in users."""
    if 'username' not in session:
        return redirect(url_for('forum_bp.login'))
    comment = request.form['comment']
    conn, cur = get_db()
    if os.environ.get('DATABASE_URL'):
        cur.execute('INSERT INTO comments (post_id, author, content) VALUES (%s, %s, %s)', (post_id, session['name'], comment))
    else:
        cur.execute('INSERT INTO comments (post_id, author, content) VALUES (?, ?, ?)', (post_id, session['name'], comment))
    conn.commit()
    conn.close()
    return redirect(url_for('forum_bp.post', post_id=post_id))

@forum_bp.route('/subscribe', methods=('POST',))
def subscribe():
    """Subscribe to the newsletter (dummy implementation)."""
    if request.method == 'POST':
        email = request.form['email']
        conn, cur = get_db()
        # You can implement actual subscription logic here
        conn.close()
        flash('Subscription successful')
        return redirect(url_for('forum_bp.index'))

@forum_bp.route('/search', methods=('GET',))
def search():
    """Search for posts by title or content."""
    query = request.args.get('q')
    conn, cur = get_db()
    if os.environ.get('DATABASE_URL'):
        cur.execute('SELECT * FROM posts WHERE title ILIKE %s OR content ILIKE %s', (f'%{query}%', f'%{query}%'))
        posts = cur.fetchall()
    else:
        cur.execute('SELECT * FROM posts WHERE title LIKE ? OR content LIKE ?', (f'%{query}%', f'%{query}%'))
        posts = cur.fetchall()
    conn.close()
    return render_template('search.html', posts=posts, query=query)

# Register the Blueprint with the /thecyberforum prefix
app.register_blueprint(forum_bp, url_prefix='/thecyberforum')

@app.route('/')
def root_redirect():
    """Redirect root URL to the /thecyberforum home page."""
    return redirect('/thecyberforum')

