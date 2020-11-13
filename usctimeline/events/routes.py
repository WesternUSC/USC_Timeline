import os
from calendar import month_name
from flask import Blueprint, flash, request, redirect, render_template, url_for
from flask_login import current_user, login_required
from sqlalchemy import and_
from usctimeline import db
from usctimeline.models import Event, Image, Tag
from usctimeline.utils import save_img_to_file_system
from usctimeline.events.forms import (EventForm, SearchEventForm, update_event_form_factory)

events = Blueprint('events', __name__)


@events.route("/event/new", methods=['GET', 'POST'])
@login_required
def new_event():
    """Route for creating a new event.

    Returns:
        A redirect to the account route inside the users module if the form
        submission is valid.
        Otherwise, a rendered HTML template for this route.
    """
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            date=form.date.data,
            description=form.description.data,
            external_url=form.external_url.data,
            category=form.category.data
        )
        if form.tags.data:
            for tag in form.tags.data:
                event.tags.append(tag)
        if form.images.data[0].filename != '':
            for image in form.images.data:
                filename, file_ext = os.path.splitext(image.filename)
                if file_ext not in ['.png', '.PNG', '.jpg', '.JPG',
                                    '.jpeg', '.JPEG', '.svg', '.SVG']:
                    flash('File does not have an approved extension:'
                          ' jpg, jpeg, png, svg', 'error')
                    return render_template(
                        'events/edit_event.html',
                        title='New Event',
                        form=form,
                        legend='New Event',
                        cancel_dest=url_for('users.account')
                    )
                else:
                    img = save_img_to_file_system(image)
                    event.images.append(img)
        db.session.add(event)
        db.session.commit()
        flash('Event has been created!', 'success')
        return redirect(url_for('events.manage_events'))
    return render_template(
        'events/edit_event.html',
        title='New Event',
        form=form,
        legend='New Event',
        cancel_dest=url_for('users.account')
    )


@events.route("/event/manage")
@login_required
def manage_events():
    """Route for managing all existing events.

    Returns:
        A rendered HTML template for this route.
    """
    events = Event.query.all()
    return render_template(
        'events/manage_events.html',
        title='Manage Events',
        events=events
    )


@events.route("/event/<int:id>")
def event(id):
    """Route for displaying a single event.

    Args:
        id: ID of the event to be displayed.

    Returns:
        A rendered HTML template for this route if an event with <id> exists.
        Otherwise, a 404 page.
    """
    current_event = Event.query.get_or_404(id)
    year = current_event.date.strftime("%Y")
    referrer = request.referrer
    if 'search' not in referrer:
        referrer = referrer + f'#{year}'
    return render_template(
        'events/event.html',
        title='single_event.title',
        event=current_event,
        referrer=referrer
    )


@events.route("/event/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_event(id):
    """Route for updating a specific event's information.

    Args:
        id: ID of the event to be updated.

    Returns:
        If the form submission is valid and an Event with <id> exists, then a
        redirect to the event route inside the events module is returned.
        If an Event with <id> does not exist, then a 404 page is returned.
        Otherwise, a rendered HTML template for this route is returned.
    """
    event = Event.query.get_or_404(id)
    UpdateEventForm = update_event_form_factory(event.category.name, event.id)
    form = UpdateEventForm()
    if form.validate_on_submit():
        event.title = form.title.data
        event.date = form.date.data
        event.description = form.description.data
        event.external_url = form.external_url.data
        event.category = form.category.data
        event.tags = form.tags.data
        if form.images.data[0].filename != '':
            for image in form.images.data:
                filename, file_ext = os.path.splitext(image.filename)
                if file_ext not in ['.png', '.PNG', '.jpg', '.JPG',
                                    '.jpeg', '.JPEG', '.svg', '.SVG']:
                    flash('File does not have an approved extension:'
                          ' jpg, jpeg, png, svg', 'error')
                    return render_template(
                        'events/edit_event.html',
                        title='Update Event',
                        form=form,
                        legend='Update Event',
                        cancel_dest=url_for('events.update_event', id=event.id)
                    )
                else:
                    img = save_img_to_file_system(image)
                    event.images.append(img)
        db.session.commit()
        flash('Event has been updated!', 'success')
        return redirect(url_for('events.event', id=event.id))
    elif request.method == 'GET':
        form.title.data = event.title
        form.date.data = event.date
        form.description.data = event.description
        form.external_url.data = event.external_url
    return render_template(
        'events/edit_event.html',
        title='Update Event',
        form=form,
        images=event.images,
        legend='Update Event',
        cancel_dest=url_for('events.event', id=event.id),
    )


@events.route('/event/<int:id>/delete')
@login_required
def delete_event(id):
    """Route for deleting a specific event.

    Args:
        id: ID of the event to be deleted.

    Returns:
        A redirect for the manage_events route inside the events module if an
        event with <id> exists.
        Otherwise, a 404 page.
    """
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    flash('Event has been deleted!', 'success')
    return redirect(url_for('events.manage_events'))


@events.route('/event/<int:id>/delete/confirm')
@login_required
def delete_event_confirmation(id):
    """Route for confirming the deletion of an event.

    Args:
        id: ID of the event to be deleted.

    Returns:
        A rendered HTML template for this route if an event with <id> exists.
        Otherwise, a 404 page.
    """
    event = Event.query.get_or_404(id)
    return render_template(
        'events/delete_event_confirmation.html',
        title='Delete Event Confirmation',
        event=event
    )


@events.route("/event/search", methods=['GET', 'POST'])
def search_event():
    """Route for searching event(s).

    Returns:
        A rendered HTML template for this route with all events matching the
        criteria provided in the SearchEventForm (if any exist).
    """
    form = SearchEventForm()
    events = []
    if form.validate_on_submit():
        title = form.title.data
        exact_date = form.exact_date.data
        from_date = form.from_date.data
        to_date = form.to_date.data
        category = form.category.data
        tags = form.tags.data
        all_events = Event.query.all()
        event_ids = set()
        for event in all_events:
            event_ids.add(event.id)
        if title:
            title_ids = set()
            result = Event.query.filter(Event.title.like(f'%{title}%')).all()
            for event in result:
                title_ids.add(event.id)
            event_ids = event_ids.intersection(title_ids)
        if exact_date:
            date_ids = set()
            result = Event.query.filter(Event.date == exact_date)
            for event in result:
                date_ids.add(event.id)
            event_ids = event_ids.intersection(date_ids)
        if from_date and to_date:
            date_ids = set()
            result = Event.query.filter(and_(
                from_date <= Event.date, Event.date <= to_date)
            ).all()
            for event in result:
                date_ids.add(event.id)
            event_ids = event_ids.intersection(date_ids)
        if category:
            category_ids = set()
            result = Event.query.filter_by(category=category).all()
            for event in result:
                category_ids.add(event.id)
            event_ids = event_ids.intersection(category_ids)
        if tags:
            for tag in tags:
                tag_ids = set()
                result = Tag.query.filter_by(name=tag.name).first()
                for event in result.events:
                    tag_ids.add(event.id)
                event_ids = event_ids.intersection(tag_ids)
        for id in event_ids:
            event = Event.query.get(id)
            events.append(event)
        if len(events) == 0:
            flash('No events found.', 'error')
    return render_template(
        'events/search_event.html',
        title='Search Event',
        form=form,
        events=events,
        month_name=month_name
    )
