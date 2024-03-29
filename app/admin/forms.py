from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, SelectField, BooleanField
from wtforms.validators import DataRequired, ValidationError, Email, NumberRange
from app.models import User

# All classes within this file use FlaskForms to generate forms that are displayed to admin users in various editing menus.
# Username and email validator functions in the user forms ensure that each username and email can only be registered once.
# Additionally, the edit user form can be initialized with the previous email and username values for the user being edited.

class EditUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    privilege_level = IntegerField('Privilege_Level', validators=[DataRequired(), NumberRange(1, 2, "Integer must be 1 or 2.")])
    submit = SubmitField('Save Changes')

    def __init__(self, o_username, o_email, *args, **kwargs):
        self.o_username = o_username
        self.o_email = o_email
        super(EditUserForm, self).__init__(*args, **kwargs)

    def validate_username(self, username):
        if username.data != self.o_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        if email.data != self.o_email:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError('Please use a different email address.')

class CreateUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', validators=[DataRequired()])
    privilege_level = IntegerField('Privilege_Level', validators=[DataRequired(), NumberRange(1, 2, "Integer must be 1 or 2.")])
    submit = SubmitField('Create User')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class SearchForm(FlaskForm):
    q= StringField('Search:')
    submit = SubmitField('Search')

# An extra note: this is the only FlaskForm done for storylets, but there are many forms that have been created in plain HTML.
class StoryletForm(FlaskForm):
    title = StringField('Title')
    image = StringField('Image')
    description = TextAreaField('Description')
    notes = TextAreaField('Notes')
    urgency = SelectField('Urgency', choices=['Low', 'Normal', 'Moderate', 'High'])
    deck = SelectField('Deck', choices=['Pinned', 'Deck', 'Unobtainable'])
    area = SelectField('Area', choices=['Temp'])
    tag = StringField('Tag')
    order = IntegerField('Order', validators=[NumberRange(min=0)])
    escapable = BooleanField('Escapable')

class QualityForm(FlaskForm):
    title = StringField('Title')
    image = StringField('Image')
    description = TextAreaField('Description')
    notes = TextAreaField('Notes')
    display = SelectField('Display', choices=['None', 'Main'])
    category = StringField('Category')
    tag = StringField('Tag')

