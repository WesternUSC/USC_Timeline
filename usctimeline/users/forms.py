from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from usctimeline.models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        'Username', validators=[
            DataRequired(),
            Length(min=2, max=20)
        ]
    )
    email = StringField(
        'Email', validators=[
            DataRequired(),
            Length(max=120),
            Email()
        ]
    )
    password = PasswordField(
        'Password', validators=[
            DataRequired(),
            Length(min=8, max=30)
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password', validators=[
            DataRequired(),
            EqualTo('password')
        ]
    )
    submit = SubmitField('Create New Account')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose another.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose another.')


class LoginForm(FlaskForm):
    email = StringField(
        'Email', validators=[
            DataRequired(),
            Email()
        ]
    )
    password = PasswordField(
        'Password', validators=[
            DataRequired(),
            Length(min=8, max=30)
        ]
    )
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField(
        'Username', validators=[
            DataRequired(),
            Length(min=2, max=20)
        ]
    )
    email = StringField(
        'Email', validators=[
            DataRequired(),
            Length(max=120),
            Email()
        ]
    )
    profile_picture = FileField(
        'Update Profile Picture',
        validators=[FileAllowed(['jpg', 'jpeg', 'png', 'svg'])]
    )
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose another.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose another.')


class RequestResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('There is no account with that email.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        'Password', validators=[
            DataRequired(),
            Length(min=8, max=30)
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password', validators=[
            DataRequired(),
            EqualTo('password')
        ]
    )
    submit = SubmitField('Reset')
