from threading import current_thread
from flask import Blueprint, abort
from flask_login import current_user
from flask.helpers import url_for
from flask.templating import render_template
from flask_login.utils import login_required
from werkzeug.utils import redirect, secure_filename
import os
from datetime import datetime

from . import db
from .forms import CreateEvent, createEditForm, CreateComment, bookEvent
from .models import Event, Category, Comment, Order, User

eventbp = Blueprint('event', __name__, url_prefix='/event')

# Page to create an event
@eventbp.route('/create', methods=['GET', 'POST'])
@login_required
def create():

    form = CreateEvent()

    if form.validate_on_submit():        
        category = Category.query.filter_by(Name = form.Category.data.upper()).first()

        print(form.CoverImage.data)
        
        if category is None:
            category = Category(
                Name = form.Category.data.upper()
            )

            db.session.add(category)
            db.session.commit()

            category = Category.query.filter_by(Name = form.Category.data.upper()).first()

        db_file_path = check_upload_file(form)

        event = Event(
            Name = form.Name.data,
            Description = form.Description.data,
            Status = "Upcoming",
            DateTime = datetime.strptime( (str(form.Date.data) + ' ' + str(form.Time.data)) , "%Y-%m-%d %H:%M:%S"),
            Cost = form.Cost.data,
            Address = form.Address.data,
            AvailableTickets = form.TotalTickets.data,
            TotalTickets = form.TotalTickets.data,
            CategoryID = category.CategoryID,
            Image = db_file_path        
        )

        db.session.add(event)
        db.session.commit()

        return redirect(url_for('main.index'))
    return render_template("event/create.html", form = form)

def check_upload_file(form):
  #get file data from form  
  fp=form.CoverImage.data
  filename=fp.filename
  #get the current path of the module file… store image file relative to this path  
  BASE_PATH=os.path.dirname(__file__)
  #upload file location – directory of this file/static/image
  upload_path=os.path.join(BASE_PATH,'static/events',secure_filename(filename))
  #store relative path in DB as image location in HTML is relative
  db_upload_path='events/' + secure_filename(filename)
  #save the file and return the db upload path  
  fp.save(upload_path)
  return db_upload_path

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
        event.Description = form.Description.data

        if form.Date.data is not None and form.Time.data is not None:
            event.DateTime = datetime.strptime( (str(form.Date.data) + ' ' + str(form.Time.data)) , "%Y-%m-%d %H:%M:%S")

        db.session.commit()

        return redirect(url_for('main.index'))

    return render_template('event/update.html', form = form, event = event)

@eventbp.route('/view/<int:id>', methods=['GET', 'POST'])
def view(id):
    event = Event.query.filter_by(EventID = id).first()

    form = CreateComment()

    if event is None:
        return abort(404)

    bookingForm = bookEvent(event)

    if form.validate_on_submit():
        comment = Comment(
            Username = current_user.Username,
            EventID = id,
            Comment = form.Content.data,
            DateTime = datetime.date(datetime.now())
        )

        db.session.add(comment)
        db.session.commit()

        return redirect(url_for('event.view', id=id))
    
    return render_template("event/view.html", event = event, form = form , bookingForm = bookingForm)

@eventbp.route('/booking/<int:id>', methods=['GET', 'POST'])
def booking(id):

    event = Event.query.filter_by(EventID = id).first()

    form = bookEvent(event)

    if form.validate_on_submit():

        order = Order(
            NumTickets = form.Amount.data,
            EventID = id,
            Username = current_user.Username
        )

        event.AvailableTickets -= form.Amount.data

        db.session.add(order)
        db.session.commit()

        return redirect(url_for('event.view', id = id))

    return redirect(url_for('event.view', id = id))    