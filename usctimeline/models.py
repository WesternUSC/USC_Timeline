from flask import current_app
from usctimeline import db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    """Retrieves a User from the database.

    Args:
        user_id: User ID

    Returns:
        An instance of User with <user_id> if it exists.
        Otherwise, None.
    """
    return User.query.get(int(user_id))

# Many-to-many relationship table between Event and Tag
event_tags = db.Table(
    'event_tags',
    db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

# Many-to-many relationship table between Event and Image
event_images = db.Table(
    'event_images',
    db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
    db.Column('image_id', db.Integer, db.ForeignKey('image.id'))
)


class User(db.Model, UserMixin):
    """Defines a User table.

    Attributes:
        id:
            Defines primary key integer column.
        username:
            Defines string column for username.
        email:
            Defines string column for email.
        password:
            Defines string column for password.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def get_reset_token(self, seconds_until_expire=1800):
        """Generates a unique, time-sensitive token for resetting password.

        Args:
            seconds_until_expire: Number of seconds until token expires.

        Returns:
            Generated token in utf-8 format.
        """
        serializer = Serializer(
            current_app.config['SECRET_KEY'],
            seconds_until_expire
        )
        return serializer.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        """Tests if token is invalid or expired.

        Args:
            token: Reset token for User

        Returns:
            If the token is valid, then an instance of User is returned.
            Otherwise, None is returned.
        """
        serializer = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = serializer.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}, '{self.email}'. '{self.profile_img}')"


class Event(db.Model):
    """Defines an Event table.

    Attributes:
        id:
            Defines primary key integer column.
        title:
            Defines string column for the event's title.
        date:
            Defines date column for the event's date.
        external_url:
            Defines text column for a URL.
        category_id:
            Defines foreign key integer column for a specific category id.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)
    external_url = db.Column(db.Text)
    category = db.Column(
        db.Integer,
        db.ForeignKey('category.id'),
        nullable=False
    )

    def __repr__(self):
        return f"Event('{self.title}', '{self.date}')"


class Image(db.Model):
    """Defines an Image table.

    Attributes:
        id:
            Defines primary key integer column.
        filename:
            Defines string column for an image filename.
        events:
            Defines foreign key id for specific row in event_images table.
            (Many-to-many relationship)
    """
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), unique=True, nullable=False)
    events = db.relationship(
        'Event',
        secondary=event_images,
        backref="images",
        lazy=True
    )

    def __repr__(self):
        return f"Image('{self.filename}')"


class Category(db.Model):
    """Defines a Category table.

    Attributes:
        id:
            Defines primary key integer column.
        name:
            Defines string column for category name.
        events:
            Defines one-to-many relationship with Events table.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    events = db.relationship('Event', backref='category', lazy=True)

    def __repr__(self):
        return f"Category('{self.name}')"


class Tag(db.Model):
    """Defines a Tag table.

    Attributes:
        id:
            Defines primary key integer column.
        name:
            Defines string column for tag name.
        events:
            Defines foreign key id for specific row in event_tags table.
            (Many-to-many relationship)
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    events = db.relationship(
        'Event',
        secondary=event_tags,
        backref="tags",
        lazy=True
    )

    def __repr__(self):
        return f"Tag('{self.name}')"
