from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, MultipleFileField, SubmitField
from wtforms.fields.html5 import DateField, URLField
from wtforms.validators import DataRequired, Optional
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from usctimeline.models import Category, Tag
from usctimeline.categories.forms import category_query
from usctimeline.tags.forms import tag_query


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
    submit = SubmitField('Submit')


def update_event_form_factory(default_category_name, event_id):
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
