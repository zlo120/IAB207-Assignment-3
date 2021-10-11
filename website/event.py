from threading import current_thread
from flask import Blueprint
from flask.helpers import url_for
from flask.templating import render_template
from werkzeug.utils import redirect
from datetime import datetime

from . import db
from .forms import CreateEvent, createEditForm
from .models import Event, Category

eventbp = Blueprint('event', __name__, url_prefix='/event')

# Page to create an event
@eventbp.route('/create', methods=['GET', 'POST'])
def create():

    form = CreateEvent()

    if form.validate_on_submit():        
        category = Category.query.filter_by(Name = form.Category.data.upper()).first()
        
        if category is None:
            category = Category(
                Name = form.Category.data.upper()
            )

            db.session.add(category)
            db.session.commit()

            category = Category.query.filter_by(Name = form.Category.data.upper()).first()

        event = Event(
            Name = form.Name.data,
            Status = "Upcoming",
            DateTime = datetime.strptime( (str(form.Date.data) + ' ' + str(form.Time.data)) , "%Y-%m-%d %H:%M:%S"),
            Cost = form.Cost.data,
            Address = form.Address.data,
            AvailableTickets = form.TotalTickets.data,
            TotalTickets = form.TotalTickets.data,
            CategoryID = category.CategoryID
            
        )

        db.session.add(event)
        db.session.commit()

        return redirect(url_for('main.index'))

    return render_template("event/create.html", form = form)

@eventbp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    event = Event.query.filter_by(EventID = id).first()

    if event is None:
        return "This event doesn't exist"
   
    form = createEditForm(event)

    if form.validate_on_submit():

        category = Category.query.filter_by(Name = form.Category.data.upper()).first()
        
        if category is None:
            category = Category(
                Name = form.Category.data.upper()
            )

            db.session.add(category)
            db.session.commit()

            category = Category.query.filter_by(Name = form.Category.data.upper()).first()


        event.Name = form.Name.data
        event.CategoryID = category.CategoryID        
        event.Cost = form.Cost.data
        event.Address = form.Address.data
        event.TotalTickets = form.TotalTickets.data

        if form.Date.data is not None and form.Time.data is not None:
            event.DateTime = datetime.strptime( (str(form.Date.data) + ' ' + str(form.Time.data)) , "%Y-%m-%d %H:%M:%S")

        db.session.commit()

        return redirect(url_for('main.index'))

    return render_template('event/update.html', form = form)

@eventbp.route('/view/<int:id>', methods=['GET', 'POST'])
def view(id):
    event = Event.query.filter_by(EventID = id).first()

    if event is None:
        return "This event doesn't exist"

    return render_template("event/view.html", event = event)