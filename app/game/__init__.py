from flask import Blueprint

bp = Blueprint('game', __name__,
    template_folder="templates",
    )

from app.game import routes