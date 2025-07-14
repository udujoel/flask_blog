# TheCyberForum

**Version: 1.1.0**

A simple blog application built with Flask that allows users to create, read, update, and delete blog posts.

---

## Changelog

### 1.1.0 (2024-07-14)
- Blog main page updated to a more traditional look with a hero image at the top.
- All routes now use `/thecyberforum` as a URL prefix via Flask Blueprint.
- Root `/` now redirects to `/thecyberforum`.
- All URLs in templates updated to use the Blueprint prefix.
- Images now referenced using Flask's `url_for('static', ...)` for robust static file serving.
- Added comment functionality to post view page.
- Added search function with a search icon in the navbar.
- Edit and delete now work for posts; only the post creator can edit or delete their posts.
- Edit and delete available from both the post view and profile page.
- Create post supports image display.
- Post view page displays pasted images.
- Contact Us page is now connected and functional.
- Improved code documentation and clarity with comments in `app.py`.

### 1.0.0 (Initial Release)
- View all blog posts on the homepage
- Create, edit, and delete blog posts
- Responsive design using Bootstrap
- User authentication (login, logout, register)
- Profile page
- Contact us form

---

## Features

- View all blog posts on the homepage
- Create new blog posts
- Edit existing blog posts (only by the post creator)
- Delete blog posts (only by the post creator)
- Add comments to posts
- Search posts by title or content
- Responsive design using Bootstrap
- User authentication (login, logout, register)
- Profile page with user's posts and quick actions
- Contact us form
- All routes under `/thecyberforum` for clear branding
- Robust static file/image handling

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/udujoel/flask-blog.git
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
   pip install flask flask-session
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

3. Open your browser and navigate to `http://127.0.0.1:5000/thecyberforum/`

## Project Structure

```
flask_blog/
├── app.py                  # Main application file
├── init_db.py              # Database initialization script
├── schema.sql              # SQL schema for the database
├── database.db             # SQLite database file
├── static/                 # Static files (CSS, JS, images)
│   ├── css/
│   ├── img/
│   └── js/
└── templates/              # HTML templates
    ├── base.html           # Base template with common elements
    ├── index.html          # Homepage template
    ├── create.html         # Create post template
    ├── edit.html           # Edit post template
    ├── post.html           # Single post template
    ├── profile.html        # User profile template
    ├── contactus.html      # Contact form template
    └── search.html         # Search results template
```

## Development

- Set `FLASK_ENV=development` to enable debug mode
- The server will automatically reload when you make changes to the code

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
