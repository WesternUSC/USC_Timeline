from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from usctimeline.models import Tag


def tag_query():
    """Returns a Flask-SQLAlchemy query object for the Tag model."""
    return Tag.query


class TagForm(FlaskForm):
    """Form for creating a new Tag object.

    Attributes:
        name:
            An input element of type text for the tag name.
        submit:
            An input element of type submit.
    """
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')
