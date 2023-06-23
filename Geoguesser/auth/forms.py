from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError 
from flask_wtf.file import FileRequired, FileAllowed
#I think something needs to be imported to activate FileAllowed and FileRequired, but I'm not sure from where.

from ..models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    firstname = StringField('Firstname', validators=[DataRequired()])
    lastname =  StringField('Lastname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    alias = StringField('Alias/Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('ConfirmPassword', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists')
    
class UpdateUserForm(FlaskForm):
    picture = FileField('Avatar', validators=[FileAllowed(['jpg', 'png', 'jfif'])])
    alias = StringField('Alias/Username', validators=[DataRequired(), Length(min=5, max=20)])
    firstname = StringField('Firstname', validators=[Length(max=50)])
    lastname =  StringField('Lastname', validators=[Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Register')
    # picture alias firstname lastname email submit
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already exists')
    
    def validate_alias(self, alias):
        if alias.data != current_user.alias:
            user = User.query.filter_by(alias=alias.data).first()
            if user:
                raise ValidationError('Username already exists')
            

class LoginForm(FlaskForm):
    username = StringField('Alias/Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class UploadGeoLocationForm(FlaskForm):
    image = FileField('Geo Location Picture', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jfif'])])
    difficulty = StringField('Difficulty', validators=[DataRequired(), Length(min=4, max=20)])
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Upload')