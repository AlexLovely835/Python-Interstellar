from app.game import bp
from app import db
from flask import render_template, request, flash
from flask_login import current_user, login_required
from app.models import Storylet, Branch, Hand
import random

@bp.route('/storylet')
@login_required
def storylet():
    id = request.args.get('id', type=int)
    storylet = db.session.query(Storylet).get(id)
    return render_template('storylet.html', storylet=storylet)

@bp.route('/results')
@login_required
def results():
    id = request.args.get('id', type=int)
    branch = db.session.query(Branch).get(id)
    storylet = branch.parent_storylet
    for results in branch.results:
        if results.type == 'General':
            result = results
        else:
            flash("No general result tied to this storylet.")
    current_user_hand_query = db.session.query(Hand).filter(Hand.user_id == current_user.id).all()
    for hand in current_user_hand_query:
        if hand.storylet == storylet:
            db.session.delete(hand)
            db.session.commit()
    return render_template('result.html', storylet=storylet, branch=branch, result=result) 

@bp.route('/game')
@login_required
def game():
    storylets = db.session.query(Storylet).filter(Storylet.deck == 'Pinned').order_by(Storylet.order).all()
    return render_template('game.html', storylets=storylets)

@bp.route('/draw')
@login_required
def draw():
    slot = request.args.get('slot', type=int)
    storylets = db.session.query(Storylet).filter(Storylet.deck == "Deck").all()
    current_user_hand_query = db.session.query(Hand).filter(Hand.user_id == current_user.id).all()
    storylets_in_hand = []
    for hand in current_user_hand_query:
        storylets_in_hand.append(hand.storylet)
        if hand.slot == slot:
            return render_template('card.html', storylet=hand.storylet)
    for card in storylets_in_hand:
        for storylet in storylets:
            if card == storylet:
                storylets.remove(storylet)
    if storylets != []:
        choice = random.choice(storylets)
        hand = Hand(user_id=current_user.id, storylet_id=choice.id, slot=slot)
        db.session.add(hand)
        db.session.commit()
        return render_template('card.html', storylet=choice)
    else: 
        return render_template('slot.html', slot=slot)

@bp.route('/load_card')
@login_required
def load_card():
    slot = request.args.get('slot', type=int)
    current_user_hand_query = db.session.query(Hand).filter(Hand.user_id == current_user.id).all()
    for hand in current_user_hand_query:
        if hand.slot == slot:
            return render_template('card.html', storylet=hand.storylet)
    if slot == 1:
        for hand in current_user_hand_query:
            if hand.slot == 2 or hand.slot == 3:
                hand.slot = 1
                db.session.commit()
                return render_template('card.html', storylet=hand.storylet)
    if slot == 2:
        for hand in current_user_hand_query:
            if hand.slot == 3:
                hand.slot = 2
                db.session.commit()
                return render_template('card.html', storylet=hand.storylet)

    
    return render_template('slot.html', slot=slot)
    