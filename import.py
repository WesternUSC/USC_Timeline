import json
from datetime import datetime
from usctimeline import create_app, db
from usctimeline.models import Event, Tag, Category


def populate_tags(path_to_file):
    with open(path_to_file) as file:
        tags = json.load(file)

    for tag in tags:
        new_tag = Tag.query.filter_by(name=tag['name']).first()
        if new_tag and new_tag.name.lower() == tag['name'].lower():
            pass  # Tag already exists
        else:
            new_tag = Tag(name=tag['name'])
            db.session.add(new_tag)
    db.session.commit()


def populate_events(path_to_file):
    with open(path_to_file) as file:
        events = json.load(file)

    event_num = 1
    for event in events:
        if not event['title']:
            raise ValueError(f"Could not import data. Title for event number {event_num} is empty.")
        if not event['date']:
            raise ValueError(f"Could not import data. Date for event number {event_num} is empty.")
        if not event['description']:
            raise ValueError(f"Could not import data. Description for event number {event_num} is empty.")
        if not event['category']:
            raise ValueError(f"Could not import data. Category for event number {event_num} is empty.")
        category = Category.query.filter_by(name=event['category']).first()
        if not category:
            raise ValueError(
                f"Could not import data. Category '{event['category']}' provided for event number {event_num} does not \
exist. Note, category names are case-sensitive."
            )
        date = datetime.strptime(event['date'], '%Y-%m-%d').date()
        new_event = Event(
            title=event['title'],
            date=date,
            description=event['description'],
            external_url=event['url'],
            category=category
        )
        tags = event['tags'].split(',')
        for name in tags:
            tag = Tag.query.filter_by(name=name).first()
            if not tag:
                raise ValueError(
                    f"Could not import data. Tag '{name}' provided for event number {event_num} caused an error or does \
not yet exist. Note, tag names are case-sensitive and should be separated by a comma without any spacing between \
names. For example, 'Science,Sports,Art'."
                )
            new_event.tags.append(tag)
            db.session.add(new_event)
    db.session.commit()


app = create_app()
with app.app_context():
    populate_tags('data/tags.json')
    populate_events('data/events.json')
