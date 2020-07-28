import os
import secrets
from calendar import month_name
from flask import render_template, url_for, flash, redirect, request
from usctimeline import app, db, bcrypt
from usctimeline.forms import RegistrationForm, LoginForm, UpdateAccountForm, EventForm, CategoryForm
from usctimeline.models import User, Event, Image, Category, Tag, event_tags, event_images
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
def index():
    events = Event.query.all()
    return render_template('timeline.html', events=events, month_name=month_name)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('account'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('You have been logged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'error')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


def save_img_to_file_system(img, dir) -> str:
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(img.filename)
    filename = random_hex + file_ext
    directory = f'static/images/{dir}'
    filepath = os.path.join(app.root_path, directory, filename)
    img.save(filepath)

    return filename


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.profile_picture.data:
            new_img_filename = save_img_to_file_system(form.profile_picture.data, 'profile')
            current_user.profile_img = new_img_filename
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    profile_img = url_for('static', filename=f'images/profile/{current_user.profile_img}')
    return render_template('account.html', title='Account', profile_img=profile_img, form=form)


@app.route("/event/new", methods=['GET', 'POST'])
@login_required
def new_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            date=form.date.data,
            description=form.description.data,
            external_url=form.external_url.data,
            author=current_user,
            category=form.category.data
        )
        if form.tags.data:
            for tag in form.tags.data:
                event.tags.append(tag)
        if form.images.data[0].filename == '':
            pass  # no images uploaded
        else:
            for image in form.images.data:
                file_ext = os.path.splitext(image.filename)[1]
                print()
                if file_ext not in ['.png', '.PNG', 'jpg', '.JPG', '.jpeg', '.JPEG', '.svg', '.SVG']:
                    flash('File does not have an approved extension: jpg, jpeg, png, svg', 'error')
                    return render_template('new_event.html', title='New Event', form=form)
            for image in form.images.data:
                new_img_filename = save_img_to_file_system(image, 'event')
                image = Image(
                    filename=new_img_filename
                )
                event.images.append(image)
        db.session.add(event)
        db.session.commit()
        flash('Event has been created!', 'success')
        return redirect(url_for('account'))
    return render_template('new_event.html', title='New Event', form=form)


@app.route("/event/manage")
@login_required
def manage_events():
    return render_template('manage_events.html', title='Manage Events')


@app.route("/category/new", methods=['GET', 'POST'])
@login_required
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash('Category has been created!', 'success')
        return redirect(url_for('account'))
    return render_template('new_category.html', title='New Category', form=form)
