from usctimeline import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_img = db.Column(db.String(20), nullable=False, default='default.svg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Event', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}, '{self.email}'. '{self.profile_img}')"


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    def __repr__(self):
        return f"Event('{self.title}', '{self.date}')"


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filepath = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f"Image('{self.filepath}')"


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    events = db.relationship('Event', backref='category', lazy=True)

    def __repr__(self):
        return f"Category('{self.name}')"


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"Category('{self.name}')"


event_tags = db.Table(
    'event_tags',
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

event_images = db.Table(
    'event_images',
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True),
    db.Column('image_id', db.Integer, db.ForeignKey('image.id'), primary_key=True)
)
