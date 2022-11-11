from app import app
from flask import render_template, request
from classes import Storylet

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/go')
def go():
    id = request.args.get('id', type=int)
    if id == 1:
        return render_template('storylet.html', storylet=Storylet())
    elif id == 0:
        return render_template('game.html')
    elif id == 2:
        storylet2 = Storylet()
        storylet2.title = "Yeehaw"
        storylet2.description = "Finally a nother storylet!"
        return render_template('storylet.html', storylet=storylet2)