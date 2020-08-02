import os
from calendar import month_name
from flask import Blueprint, flash, request, redirect, render_template, url_for
from flask_login import current_user, login_required
from sqlalchemy import and_
from usctimeline import db
from usctimeline.models import Event, Image, Tag
from usctimeline.utils import save_img_to_file_system
from usctimeline.events.forms import EventForm, SearchEventForm, update_event_form_factory

events = Blueprint('events', __name__)


@events.route("/event/new", methods=['GET', 'POST'])
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
                if file_ext not in ['.png', '.PNG', 'jpg', '.JPG', '.jpeg', '.JPEG', '.svg', '.SVG']:
                    flash('File does not have an approved extension: jpg, jpeg, png, svg', 'error')
                    return render_template(
                        'events/edit_event.html',
                        title='New Event',
                        form=form,
                        legend='New Event',
                        cancel_dest=url_for('users.account')
                    )
            for image in form.images.data:
                new_img_filename = save_img_to_file_system(image, 'event')
                image = Image(
                    filename=new_img_filename
                )
                event.images.append(image)
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
    events = Event.query.all()
    return render_template(
        'events/manage_events.html',
        title='Manage Events',
        events=events
    )


@events.route("/event/<int:id>")
def event(id):
    current_event = Event.query.get_or_404(id)
    return render_template('events/event.html', title='single_event.title', event=current_event)


@events.route("/event/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_event(id):
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
        db.session.commit()
        flash('Event has been updated!', 'success')
        return redirect(url_for('events.event', id=event.id))
    elif request.method == 'GET':
        form.title.data = event.title
        form.date.data = event.date
        form.description.data = event.description
    return render_template(
        'events/edit_event.html',
        title='Update Event',
        form=form,
        legend='Update Event',
        cancel_dest=url_for('events.event', id=event.id),
    )


@events.route('/event/<int:id>/delete')
@login_required
def delete_event(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    flash('Event has been deleted!', 'success')
    return redirect(url_for('events.manage_events'))


@events.route('/event/<int:id>/delete/confirm')
@login_required
def delete_event_confirmation(id):
    event = Event.query.get_or_404(id)
    return render_template('events/delete_event_confirmation.html', title='Delete Event Confirmation', event=event)


@events.route("/event/search", methods=['GET', 'POST'])
def search_event():
    form = SearchEventForm()
    events = []
    if form.validate_on_submit():
        title = form.title.data
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
        if from_date and to_date:
            date_ids = set()
            result = Event.query.filter(
                and_(from_date <= Event.date, Event.date <= to_date)
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
    return render_template(
        'events/search_event.html',
        title='Search Event',
        form=form,
        events=events,
        month_name=month_name
    )
