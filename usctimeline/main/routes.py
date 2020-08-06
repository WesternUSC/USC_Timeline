from flask import Blueprint, render_template
from usctimeline.models import Event
from calendar import month_name
from datetime import datetime

main = Blueprint('main', __name__)


@main.route("/")
def index():
    all_events = Event.query.order_by(Event.date.asc())
    events_per_year = {}
    for event in all_events:
        year = event.date.strftime("%Y")
        if year not in events_per_year:
            events_per_year[year] = {
                1: [],
                2: [],
                3: [],
                4: [],
                5: [],
                6: [],
                7: [],
                8: [],
                9: [],
                10: [],
                11: [],
                12: [],
            }
            for month in events_per_year[year]:
                if month == int(event.date.strftime("%-m")):
                    events_per_year[year][month].append(event)
        else:
            for month in events_per_year[year]:
                if month == int(event.date.strftime("%-m")):
                    events_per_year[year][month].append(event)
    return render_template('main/timeline.html', events_per_year=events_per_year, month_name=month_name)
