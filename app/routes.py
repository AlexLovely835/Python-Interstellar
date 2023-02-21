from app import app, db
from datetime import datetime
from flask import render_template
from flask_login import current_user, login_required


# This renders the main index page and redirects anyone that's not logged in to the login page instead.
@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html')

# This renders the notification top bar above main page content.
@app.route('/flash_notifs')
def flash_notifs():
    return render_template('flash_notifs.html')

# This checks that a user is logged in and updates when they were last online.
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_online = datetime.utcnow()
        db.session.commit()