from app import app, db
from datetime import datetime
from flask import render_template
from flask_login import current_user, login_required

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html')

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_online = datetime.utcnow()
        db.session.commit()