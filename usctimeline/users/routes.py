from flask import Blueprint, flash, redirect, render_template, url_for, request
from flask_login import login_required, login_user, current_user, logout_user
from usctimeline import bcrypt, db
from usctimeline.models import User, Event
from usctimeline.utils import save_img_to_file_system, send_reset_email
from usctimeline.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetPasswordForm, ResetPasswordForm

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
@login_required
def register():
    """Route for creating a new user account.

    Returns:
        If the form submission is valid then a redirect to the account route
        in the users module is returned.
        Otherwise, an HTML template for this route is returned.
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data
        ).decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('users.account'))
    return render_template('users/register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    """Route for logging in to a user account.

    Returns:
        If the user is already logged in, then a redirect to the account route
        in the users module is returned.
        If the form submission is valid and the email/password is correct, then
        a redirect to the index route in the main module is returned.
        Otherwise, an HTML template for this route is returned.
    """
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
                user.password,
                form.password.data
        ):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('You have been logged in!', 'success')
            return (redirect(next_page)
                    if next_page
                    else redirect(url_for('main.index'))
                    )
        else:
            flash(
                'Login unsuccessful. Please check email and password.', 'error'
            )
    return render_template('users/login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    """Route for logging out a user.

    Returns:
        A redirect to the index route in the main module.
    """
    logout_user()
    return redirect(url_for('main.index'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    """Route for user account page.

    Form is provided to update username and/or email.

    Returns:
        If form submission is valid, then the users username/email is updated in
        the database, and a redirect to this same route is returned.
        If the request method for this route is 'GET', then an HTML template
        for this route is returned.
    """
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('users/account.html', title='Account', form=form)


@users.route("/forgot", methods=['GET', 'POST'])
def reset_request():
    """Route for requesting a password reset.

    Returns:
        If the user is already logged in, then a redirect to the index route
        in the main module is returned.
        If the form submission is valid, then a redirect to the login route in
        the users module is returned.
        Otherwise, an HTML template for this route is returned.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RequestResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(
            'An email has been sent with instructions to reset your password.',
            'success'
        )
        return redirect(url_for('users.login'))
    return render_template(
        'users/reset_request.html',
        title='Request Password Reset',
        form=form
    )


@users.route("/reset/<token>", methods=['GET', 'POST'])
def reset_password(token):
    """Route for resetting a password.

    Args:
        token: Unique, time-sensitive token generated in User model for allowing
            password reset.

    Returns:
        If the user is already logged in, then a redirect to the index route in
        the main module is returned.
        If the token is invalid or expired, then a redirect to the reset_request
        route in the users module is returned.
        If the form submission is valid, then a redirect to the account route
        in the users module is returned.
        Otherwise, an HTML template is rendered for this route is returned.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired.', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data
        ).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        login_user(user)
        flash('Your password has been updated!', 'success')
        return redirect(url_for('users.account'))
    return render_template(
        'users/reset_password.html',
        title='Reset Password',
        form=form
    )
