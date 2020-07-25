from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from usctimeline.models import User
from typing import Union


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
    submit = SubmitField('Sign Up')

    def validate_username(self, username) -> None:
        user: Union[None, str] = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose another.')

    def validate_email(self, email) -> None:
        user: Union[None, str] = User.query.filter_by(email=email.data).first()
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
        'Update Profile Picture', validators=[
            FileAllowed(['jpg', 'jpeg', 'png', 'svg'])
        ]
    )
    submit = SubmitField('Update')

    def validate_username(self, username) -> None:
        if username.data != current_user.username:
            user: Union[None, str] = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose another.')

    def validate_email(self, email) -> None:
        if email.data != current_user.email:
            user: Union[None, str] = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose another.')
