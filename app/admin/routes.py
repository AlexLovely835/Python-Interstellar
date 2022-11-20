from app.admin import bp
from app import db
from flask import redirect, render_template, request, url_for, flash
from flask_login import current_user, login_required
from app.models import User, Storylet, Branch
from app.admin.forms import EditUserForm, CreateUserForm, SearchForm, StoryletForm
from app.admin.classes import PageResult, Tag, defaultStorylet

@bp.route('/')
@login_required
def admin():
    if current_user.privilege_level > 1:
        return render_template('admin.html')
    else:
        return redirect(url_for('index'))

@bp.route('/storylets')
@login_required
def storylets():
    if current_user.privilege_level > 1:

        #Construct a list of Tags and their Storylets
        tag_list = db.session.query(Storylet.tag.distinct().label("tag")).all()
        tags = []
        for tag in tag_list:
            print(tag)
            tag = str(tag).replace('(', '').replace(')', '').replace(',', '').replace("'", "")
            if tag == 'None':
                tags.append(Tag(None))
            else:
                tags.append(Tag(tag))

        #Grab a list of the most recently edited Storylets
        recents = db.session.query(Storylet).order_by(Storylet.last_edit).limit(5).all()

        return render_template('storylets.html', recents=recents, tags=tags)
    else:
        return redirect(url_for('index'))

@bp.route('/edit_storylet')
@login_required
def edit_storylet():
    if current_user.privilege_level > 1:
        id = request.args.get('id', None, type=int)
        form = StoryletForm()
        if id == None:
            storylet = defaultStorylet()
            storylet.user_id = current_user.id
            db.session.add(storylet)
            db.commit()
            storylet = db.session.query(Storylet).order_by(Storylet.last_edit).limit(1).all()
        else:
            storylet = db.session.query(Storylet).get(id)
        form.title.data = storylet.title
        form.image.data = storylet.image
        form.description.data = storylet.description
        form.notes.data = storylet.notes
        form.urgency.data = storylet.notes
        form.deck.data = storylet.deck
        form.area.data = storylet.area
        form.tag.data = storylet.tag
        form.escapable.data = storylet.escapable

        return render_template('edit_storylet.html', form=form, storylet=storylet)
    else:
        return redirect(url_for('index'))

@bp.route('/users/<pagenum>', methods=['GET', 'POST'])
@login_required
def users(pagenum):
    if current_user.privilege_level > 1:

        # Initiate forms and arguments
        form = SearchForm()
        result = False
        search = request.args.get('search', None, type=str)

        # Determine if the page is acting as a search function
        if form.q.data != None:
            query = form.q.data
            users = db.session.query(User).filter(User.username.ilike("%"+query+"%")).all()
            result = True
        elif search != None:
            users = db.session.query(User).filter(User.username.ilike("%"+search+"%")).all()
            result = True
            form.q.data = search
        else:
            users = db.session.query(User).order_by(User.last_online.desc()).all()

        # Determine if the next page exists
        if len(users) <= (int(pagenum)-1) * 20:
            return redirect(url_for('admin.users', pagenum=int(pagenum)-1, search=search))

        #Determine if a search result yields no result
        if len(users) == 0:
            flash("No search results found.")
            return redirect(url_for('admin.users', pagenum=1))

        #Return
        return render_template('users.html', listing=PageResult(users, int(pagenum)), form=form, result=result, query=form.q.data)
    else:
        return redirect(url_for('index'))

@bp.route('/create_user', methods=['GET', 'POST'])
@login_required
def create_user():
    if current_user.privilege_level > 1:
        form = CreateUserForm()
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data, privilege_level=form.privilege_level.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('User created.')
            return redirect(url_for('admin.users', pagenum=1))
        return render_template('create_user.html', form=form)
    else:
        return redirect(url_for('index'))


@bp.route('/edit_user', methods=['GET', 'POST'])
@login_required
def edit_user():
    if current_user.privilege_level > 1:
        id = request.args.get('id', type=int)
        user = db.session.query(User).get(id)
        form = EditUserForm(user.username, user.email)
        if form.validate_on_submit():
            user.username = form.username.data
            user.email = form.email.data
            user.privilege_level = form.privilege_level.data
            db.session.commit()
            flash('Your changes have been saved.')
            return redirect(url_for('admin.edit_user', id=user.id))
        elif request.method == 'GET':
            form.username.data = user.username
            form.email.data = user.email
            form.privilege_level.data = user.privilege_level
        return render_template('edit_user.html', user=user, form=form)
    else:
        return redirect(url_for('index'))

@bp.route('/delete_user')
@login_required
def delete_user():
    if current_user.privilege_level > 1:
        id = request.args.get('id', type=int)
        user = db.session.query(User).get(id)
        db.session.delete(user)
        db.session.commit()
        flash("User deleted.")
        return redirect(url_for('admin.users', pagenum=1))
    else:
        return redirect(url_for('index'))