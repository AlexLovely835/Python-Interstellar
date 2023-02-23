import os
from app.admin import bp
from app import db, app
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import redirect, render_template, request, url_for, flash
from flask_login import current_user, login_required
from app.models import User, Storylet, Branch, Result, Image
from app.admin.forms import EditUserForm, CreateUserForm, SearchForm, StoryletForm
from app.admin.classes import PageResult, Tag, defaultStorylet, defaultBranch, defaultResult, allowed_file

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
        tab = request.args.get('tab', 'all', type=str)


        #Construct a list of Tags and their Storylets
        tags = []
        if tab == 'all':
            tag_list = db.session.query(Storylet.tag.distinct().label("tag")).all()
        
            for tag in tag_list:
                tag = str(tag).replace('(', '').replace(')', '').replace(',', '').replace("'", "")
                if tag == 'None':
                    tags.append(Tag(None, 0))
                else:
                    tags.append(Tag(tag, 0))
        elif tab == 'user':
            tag_list = db.session.query(Storylet.tag.distinct().label("tag")).filter(Storylet.user_id == current_user.id).all()

            for tag in tag_list:
                tag = str(tag).replace('(', '').replace(')', '').replace(',', '').replace("'", "")
                if tag == 'None':
                    tags.append(Tag(None, current_user.id))
                else:
                    tags.append(Tag(tag, current_user.id))

        tags.sort()

        #Grab a list of the most recently edited Storylets
        recents = db.session.query(Storylet).order_by(Storylet.last_edit.desc()).limit(5).all()

        return render_template('storylets.html', recents=recents, tags=tags, tab=tab)
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
            db.session.commit()
            storylet = db.session.query(Storylet).get(storylet.id)
        else:
            storylet = db.session.query(Storylet).get(id)
        form.title.data = storylet.title
        form.image.data = storylet.image
        form.description.data = storylet.description
        form.notes.data = storylet.notes
        form.urgency.data = storylet.urgency
        form.deck.data = storylet.deck
        form.area.data = storylet.area
        form.tag.data = storylet.tag
        form.escapable.data = storylet.escapable
        form.order.data = storylet.order
        return render_template('edit_storylet.html', form=form, storylet=storylet)
    else:
        return redirect(url_for('index'))

@bp.route('/save_storylet', methods=['POST', 'GET'])
@login_required
def save_storylet():
    id = request.args.get('id', type=int)
    storylet = db.session.query(Storylet).get(id)
    storylet.title = request.form.get("title")
    storylet.image = request.form.get("image")
    storylet.description = request.form.get("description")
    storylet.notes = request.form.get("notes")
    storylet.urgency = request.form.get("urgency")
    storylet.deck = request.form.get("deck")
    storylet.area = request.form.get("area")
    tag = request.form.get("tag")
    tag.strip()
    if tag == "":
        storylet.tag = None
    else:
        storylet.tag = request.form.get("tag")
    if request.form.get("order") != '':
        storylet.order = int(request.form.get("order"))
    else:
        storylet.order = None
    if request.form.get("escapable") == 'true':
        storylet.escapable = True
    else:
        storylet.escapable = False
    storylet.last_editor = current_user.username
    storylet.last_edit = datetime.utcnow()
    db.session.commit()
    flash("Your changes have been saved.")
    return redirect(url_for('flash_notifs'))

@bp.route('/save_branch', methods=['POST', 'GET'])
@login_required
def save_branch():
    id = request.args.get('id', type=int)
    branch = db.session.query(Branch).get(id)
    branch.title = request.form.get("title")
    branch.image = request.form.get("image")
    branch.description = request.form.get("description")
    branch.notes = request.form.get("notes")
    branch.button_text = request.form.get("button_text")
    if request.form.get("order") != '':
        branch.order = int(request.form.get("order"))
    else:
        branch.order = None
    if request.form.get("action_cost") != '':
        branch.action_cost = int(request.form.get("action_cost"))
    else:
        branch.action_cost = None
    branch.parent_storylet.last_editor = current_user.username
    branch.parent_storylet.last_edit = datetime.utcnow()
    db.session.commit()
    flash("Your changes have been saved.")
    return redirect(url_for('flash_notifs'))

@bp.route('/save_result', methods=['POST', 'GET'])
@login_required
def save_result():
    id = request.args.get('id', type=int)
    result = db.session.query(Result).get(id)
    result.title = request.form.get("title")
    result.description = request.form.get("description")
    result.notes = request.form.get("notes")
    result.type = request.form.get("type")
    result.area_change = request.form.get("area_change")
    if request.form.get("next_id") != '':
        result.next_id = int(request.form.get("next_id"))
    else:
        result.next_id = None
    if request.form.get("random_weight") != '':
        result.random_weight = int(request.form.get("random_weight"))
    else:
        result.random_weight = None
    result.parent_branch.parent_storylet.last_editor = current_user.username
    result.parent_branch.parent_storylet.last_edit = datetime.utcnow()
    db.session.commit()
    flash("Your changes have been saved.")
    return redirect(url_for('flash_notifs'))

@bp.route('/create_branch', methods=['GET', 'POST'])
@login_required
def create_branch():
    id = request.args.get('id', type=int)
    branch = defaultBranch()
    branch.storylet_id = id
    db.session.add(branch)
    db.session.commit()
    return redirect(url_for('admin.create_result', s_id=id, b_id=branch.id))

@bp.route('/create_result', methods=['POST', 'GET'])
@login_required
def create_result():
    s_id = request.args.get('s_id', type=int)
    b_id = request.args.get('b_id', type=int)
    result = defaultResult()
    result.branch_id = b_id
    db.session.add(result)
    db.session.commit()
    return redirect(url_for('admin.edit_storylet', id = s_id))

@bp.route('/delete_storylet', methods=['POST', 'GET'])
@login_required
def delete_storylet():
    if current_user.privilege_level > 1:
        id = request.args.get('id', type=int)
        storylet = db.session.query(Storylet).get(id)
        for branch in storylet.branches:
            for result in branch.results:
                db.session.delete(result)
            db.session.delete(branch)
        db.session.delete(storylet)
        db.session.commit()
        flash("Storylet deleted.")
        return redirect(url_for('admin.storylets'))
    else:
        return redirect(url_for('index'))
    
@bp.route('/delete_branch', methods=['POST', 'GET'])
@login_required
def delete_branch():
    if current_user.privilege_level > 1:
        s_id = request.args.get('s_id', type=int)
        b_id = request.args.get('b_id', type=int)
        branch = db.session.query(Branch).get(b_id)
        for result in branch.results:
            db.session.delete(result)
        db.session.delete(branch)
        db.session.commit()
        flash("Branch deleted.")
        return redirect(url_for('admin.edit_storylet', id=s_id))
    else:
        return redirect(url_for('index'))
    
@bp.route('/delete_result', methods=['POST', 'GET'])
@login_required
def delete_result():
    if current_user.privilege_level > 1:
        s_id = request.args.get('s_id', type=int)
        r_id = request.args.get('r_id', type=int)
        result = db.session.query(Result).get(r_id)
        db.session.delete(result)
        db.session.commit()
        flash("Result deleted.")
        return redirect(url_for('admin.edit_storylet', id=s_id))
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
    
@bp.route('/images', methods=['GET', 'POST'])
@login_required
def images():
    if current_user.privilege_level > 1:
        if request.method == 'POST':
            if 'file' not in request.files:
                flash("No file uploaded.")
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash("No file selected.")
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
                flash("File successfully uploaded.")
                new_image = Image(name=str(filename))
                db.session.add(new_image)
                db.session.commit()
        image = db.session.query(Image).order_by(Image.name).all()
        return render_template('images.html', images=image)
    else:
        return redirect(url_for('index'))

@bp.route('/delete_image', methods=['GET', 'POST'])
@login_required
def delete_image():
    if current_user.privilege_level > 1:
        id = request.args.get('id', type=int)
        image = db.session.query(Image).get(id)
        flash("Image '{}' successfully deleted.".format(image.name))
        os.remove(os.path.join(app.config['UPLOAD_PATH'], image.name))
        db.session.delete(image)
        db.session.commit()
        
        return redirect(url_for('admin.images'))
    else:
        return redirect(url_for('index'))