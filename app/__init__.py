from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Define app and config file
app = Flask(__name__, template_folder="templates")
app.config.from_object(Config)

# Set up database and database migration tool.
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Set up login manager. 
login = LoginManager(app)
login.login_view = 'auth.login'

# Register blueprints for website subdivisions.
from app.auth import bp as auth_bp
app.register_blueprint(auth_bp)
from app.admin import bp as admin_bp
app.register_blueprint(admin_bp, url_prefix='/admin')
from app.game import bp as game_bp
app.register_blueprint(game_bp)

from app import routes
from app import models