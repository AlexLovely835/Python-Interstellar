from flask import Blueprint

# Creates a blueprint for the administration portion of the site.
bp = Blueprint('admin', __name__,
    template_folder="templates",
    static_folder="static"
    )

from app.admin import routes