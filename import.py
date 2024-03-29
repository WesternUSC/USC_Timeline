"""Script for importing new events from a JSON file.

When executing this script you must provide the path of a JSON file which
contains the event information. This file should be stored inside of
`USC_Timeline/data/json/` prior to executing the command. Otherwise, a FileNotFound
error will occur.

How to execute this script:
`python import.py data/json/filename.json`

(Where filename.json is `USC_Timeline/data/filename.json` and stores the event
data.)
"""

import sys
import json
from datetime import datetime
from usctimeline import create_app, db
from usctimeline.models import Event, Tag, Category


def create_categories():
    CATEGORIES = ['USC', 'Statistics', 'Culture']
    for name in CATEGORIES:
        category = Category(name=name)
        db.session.add(category)
    db.session.commit()


def add_events(events):
    """Add events to the database.

    Args:
        events: Dictionary of events to be added.

    Returns:
        True if events have been successfully uploaded to database.
        None, otherwise.

    Raises:
        ValueError: An error occurred query the database for category.
    """
    for event in events:
        category = Category.query.filter_by(name=event['Category']).first()
        if not category:
            raise ValueError(f"Category '{event['Category']}' not found.")
        date = datetime.strptime(event['Date'], '%Y-%m-%d').date()
        new_event = Event(
            title=event['Title'],
            date=date,
            description=event['Description'],
            external_url=event['URL'],
            category=category
        )
        if event['Tag']:
            tags = event['Tag'].split(',')
            for name in tags:
                tag = Tag.query.filter_by(name=name).first()
                if not tag:
                    raise ValueError(f"Tag '{name}' not found.")
                new_event.tags.append(tag)
        db.session.add(new_event)
    db.session.commit()
    return True


def main():
    """Opens file passed in as arg and converts data to dictionary of events.

    Returns:
        None
    """
    try:
        with open(sys.argv[1]) as file:
            events = json.load(file)
        if Category.query.count() != 3:
            create_categories()
        isUploaded = add_events(events)
        if isUploaded:
            print('Events uploaded successfully.')
    except IndexError as e:
        print(
            f'''
    IndexError: {e}

    This script requires a JSON file holding event data. 
    (JSON file needs to be stored inside `USC_Timeline/data`)
        `python import.py filename.json`

    (The above command will upload events stored in `USC_Timeline/data/filename.json`)
'''
        )
    except FileNotFoundError as e:
        print("Error: File not found.")


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        main()
