from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, MultipleFileField
from wtforms.fields.html5 import DateField, URLField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from usctimeline.models import User, Category, Tag
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
        'Update Profile Picture',
        validators=[FileAllowed(['jpg', 'jpeg', 'png', 'svg'])]
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


def category_query():
    return Category.query


def tag_query():
    return Tag.query


class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    date = DateField(
        'Date',
        validators=[DataRequired()],
        format='%Y-%m-%d'
    )
    description = TextAreaField('Description', validators=[DataRequired()])
    external_url = URLField('External URL')
    category = QuerySelectField(
        'Category',
        validators=[DataRequired()],
        query_factory=category_query,
        get_label='name',
        allow_blank=True,
        blank_text='Choose Category'
    )
    tags = QuerySelectMultipleField(
        'Tag(s)',
        query_factory=tag_query,
        get_label='name'
    )
    images = MultipleFileField('Image(s)')
    submit = SubmitField('Create')


class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Create')
