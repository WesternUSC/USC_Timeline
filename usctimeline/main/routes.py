from flask import Blueprint, render_template
from usctimeline.models import Event
from calendar import month_name

main = Blueprint('main', __name__)


@main.route("/")
def index():
    events = Event.query.order_by(Event.date.asc())
    return render_template('timeline.html', events=events, month_name=month_name)
