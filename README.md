# Flask Blog

A simple blog application built with Flask that allows users to create, read, update, and delete blog posts.

## Features

- View all blog posts on the homepage
- Create new blog posts
- Edit existing blog posts
- Delete blog posts
- Responsive design using Bootstrap

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/flask-blog.git
   cd flask-blog
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the required packages:
   ```
   pip install flask
   ```

4. Initialize the database:
   ```
   python init_db.py
   ```

## Running the Application

1. Set the Flask environment variables:
   ```
   # On Windows
   set FLASK_APP=app.py
   set FLASK_ENV=development
   
   # On macOS/Linux
   export FLASK_APP=app.py
   export FLASK_ENV=development
   ```

2. Start the development server:
   ```
   flask run
   ```

3. Open your browser and navigate to `http://127.0.0.1:5000/`

## Project Structure

```
flask_blog/
├── app.py                  # Main application file
├── init_db.py              # Database initialization script
├── schema.sql              # SQL schema for the database
├── database.db             # SQLite database file
├── static/                 # Static files (CSS, JS)
│   └── css/
│       └── style.css
└── templates/              # HTML templates
    ├── base.html           # Base template with common elements
    ├── index.html          # Homepage template
    ├── create.html         # Create post template
    ├── edit.html           # Edit post template
    └── post.html           # Single post template
```

## Development

To make changes to the application:

1. Ensure you have set `FLASK_ENV=development` to enable debug mode
2. The server will automatically reload when you make changes to the code

## Deployment

For production deployment, consider using a production WSGI server like Gunicorn or uWSGI instead of the built-in Flask server.

Example with Waitress (a production WSGI server):

1. Install Waitress:
   ```
   pip install waitress
   ```

2. Run the application:
   ```
   waitress-serve --host=0.0.0.0 --port=8000 app:app
   ```

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Bootstrap Documentation](https://getbootstrap.com/docs/4.3/getting-started/introduction/)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
