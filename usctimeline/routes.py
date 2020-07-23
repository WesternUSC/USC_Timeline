from flask import render_template, url_for, flash, redirect
from usctimeline import app
from usctimeline.forms import RegistrationForm, LoginForm
from usctimeline.models import User, Event, Image, Category, Tag, event_tags, event_images


@app.route("/")
def index():
    return render_template('timeline.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check username and password.', 'error')
    return render_template('login.html', title='Login', form=form)
