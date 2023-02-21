from flask import Blueprint

# Creates a blueprint for the authentication portion of the site.
bp = Blueprint('auth', __name__,
    template_folder="templates"
    )

from app.auth import routes