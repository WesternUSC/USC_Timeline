from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from usctimeline.models import User


class RegistrationForm(FlaskForm):
    """Form for registering a new user account.

    Attributes:
        username:
            An input element of type text for the user's username.
        email:
            An input element of type email for the user's email.
        password:
            An input element of type password for the user's password.
        confirm_password:
            An input element of type password to confirm the user's password.
        submit:
            An input element of type submit.
    """
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
    submit = SubmitField('Create')

    def validate_username(self, username):
        """Checks to see that username does not already exist.

        Args:
            username: New user's username of choice.

        Returns:
            None

        Raises:
            ValidationError: Username has already been taken.
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken. Please choose another.'
            )

    def validate_email(self, email):
        """Checks to see that email does not already exist.

        Args:
            email: New user's email of choice.

        Returns:
            None

        Raises:
            ValidationError: Email has already been taken.
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose another.')


class LoginForm(FlaskForm):
    """Form for users to log in to their account.

    Attributes:
        email:
            An input element of type email for the user's email.
        password:
            An input element of type password for the user's password.
        submit:
            An input element of type submit.
    """
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
    """A form for updating an existing user's account information.


    Attributes:
        username:
            An input element of type text for the user's username.
        email:
            An input element of type email for the user's email.
        submit:
            An input element of type submit.
    """
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
    submit = SubmitField('Update')

    def validate_username(self, username):
        """Checks to see that username does not already exist.

        Args:
            username: User's updated username.

        Returns:
            None

        Raises:
            ValidationError: Username has already been taken.
        """
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'That username is taken. Please choose another.'
                )

    def validate_email(self, email):
        """Checks to see that email does not already exist.

        Args:
            email: User's updated email.

        Returns:
            None

        Raises:
            ValidationError: Email has already been taken.
        """
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'That email is taken. Please choose another.'
                )


class RequestResetPasswordForm(FlaskForm):
    """Form to request a password reset.

    Attributes:
        email:
            An input element of type email for the user's email.
        submit:
            An input element of type submit.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        """Validates a User account with <email> exists.

        Args:
            email: User's email.

        Returns:
            None

        Raises:
            ValidationError: There is no User instance with the provided email.
        """
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('There is no account with that email.')


class ResetPasswordForm(FlaskForm):
    """A form to reset a User's password.

    Attributes:
        password:
            An input element of type password for the user's password.
        confirm_password:
            An input element of type password to confirm the user's password.
    """
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
