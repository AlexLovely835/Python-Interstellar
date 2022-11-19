from app.game import bp
from app import db
from flask import render_template, request
from flask_login import current_user, login_required
from classes import storylets, branches
import random

@bp.route('/storylet')
@login_required
def storylet():
    id = request.args.get('id', type=int)
    for storylet in storylets:
        if storylet.id == id:
            return render_template('storylet.html', storylet=storylet)

@bp.route('/results')
@login_required
def results():
    id = request.args.get('id', type=int)
    for branch in branches:
        if branch.id == id:
            for storylet in storylets:
                if storylet.id == branch.parent_id:
                    result = branch.results['General']
                    return render_template('result.html', storylet=storylet, branch=branch, result=result) 

@bp.route('/game')
@login_required
def game():
    render = []
    for storylet in storylets:
        if storylet.available == 'Always':
            render.append(storylet)
    return render_template('game.html', storylets=render)

@bp.route('/draw')
@login_required
def draw():
    choices = []
    for storylet in storylets:
        if storylet.available == 'Sometimes':
            choices.append(storylet)
    if choices != []:
        choice = random.choice(choices)
        return render_template('card.html', storylet=choice)
    else: 
        slot = request.args.get('slot', type=int)
        return render_template('slot.html', slot=slot)
