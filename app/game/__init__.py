from flask import Blueprint

# Creates a blueprint for the game function portion of the site.
bp = Blueprint('game', __name__,
    template_folder="templates",
    )

from app.game import routes