from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, MultipleFileField, SubmitField
from wtforms.fields.html5 import DateField, URLField
from wtforms.validators import DataRequired, Optional
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from usctimeline.models import Category, Tag
from usctimeline.tags.forms import tag_query

def category_query():
    """Returns a Flask-SQLAlchemy query object for the Category model."""
    return Category.query

class EventForm(FlaskForm):
    """Creates a form for creating a new Event object.

    Attributes:
        title:
            An input element of type text for the event title.
        date:
            An input element of type date for the event date.
        description:
            An input element of type text for the event description.
        external_url:
            An input element of type url for the event 'learn more' button.
        category:
            A select element for the event category.
        tags:
            A select element with multiple attribute for the event tag(s).
        images:
            An input element of type file for the event image(s).
        submit:
            An input element of type submit to submit the form.
    """

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
    submit = SubmitField('Submit')


def update_event_form_factory(default_category_name, event_id):
    """Returns a new instance of UpdateEventForm.

    Creates a new instance of UpdateEventForm. This class inherits EventForm
    and overwrites the category and tags fields of an existing Event.

    Args:
        default_category_name:
            Category name of an existing Event. This category name will be
            pre-selected in the category select element.
        event_id:
            ID of an existing event. Needed to retrieve all tag(s) (if any) for
            the Event of interest. If any tag(s) belong to the Event, then they
            will be pre-selected in the tags select element.
    Returns:
        An instance of UpdateEventForm.
    """
    class UpdateEventForm(EventForm):
        category = QuerySelectField(
            'Update Category',
            validators=[DataRequired()],
            query_factory=category_query,
            get_label='name',
            allow_blank=True,
            blank_text='Choose Category',
            default=Category.query.filter_by(name=default_category_name).first()
        )
        tags = QuerySelectMultipleField(
            'Update Tag(s)',
            query_factory=tag_query,
            get_label='name',
            default=Tag.query.filter(Tag.events.any(id=event_id)).all()
        )
        submit = SubmitField('Update')

    return UpdateEventForm


class SearchEventForm(FlaskForm):
    """Creates a form for searching specific event(s) in the database.

    Attributes:
        title:
            An input element of type text for the event title.
        exact_date:
            An input element of type date. Represents a day on which an event
            occurred.
        from_date:
            An input element of type date. Represents a day on which an event
            occurred on or after. Meant to provide a date range in conjunction
            with to_date field.
        to_date:
            An input element of type date. Represents a day on which an event
            occurred on or before. Meant to provide a date range in conjunction
            with from_date field.
        category:
            A select element for the event category.
        tags:
            A select element with multiple attribute for the event tag(s).
        submit:
            An input element of type submit to submit the form.
    """
    title = StringField('Title')
    exact_date = DateField(
        'On This Exact Day:',
        validators=[Optional()],
        format='%Y-%m-%d'
    )
    from_date = DateField(
        'From',
        validators=[Optional()],
        format='%Y-%m-%d'
    )
    to_date = DateField(
        'To',
        validators=[Optional()],
        format='%Y-%m-%d'
    )
    category = QuerySelectField(
        'Category:',
        query_factory=category_query,
        get_label='name',
        allow_blank=True,
        blank_text='None'
    )
    tags = QuerySelectMultipleField(
        'Tag(s):',
        query_factory=tag_query,
        get_label='name'
    )
    submit = SubmitField('Search')
