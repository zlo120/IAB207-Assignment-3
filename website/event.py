from threading import current_thread
from flask import Blueprint, abort, flash
from flask_login import current_user
from flask.helpers import url_for
from flask.templating import render_template
from flask_login.utils import login_required
from werkzeug.utils import redirect, secure_filename
import os
from datetime import datetime

from website.auth import login

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

        event_datetime = datetime.strptime( (str(form.Date.data) + ' ' + str(form.Time.data)) , "%Y-%m-%d %H:%M:%S")
        
        if event_datetime < datetime.now() :
            flash("You can't create an event for the past!")
            return redirect(url_for('event.create'))

        if category is None:
            category = Category(
                Name = form.Category.data.upper().replace(' ', '_')
            )

            print(f'\n\n\n{category}\n\n\n')

            db.session.add(category)
            db.session.commit()

        db_file_path = check_upload_file(form)

        print(f'\n\n\n{category}\n\n\n')

        event = Event(
            Name = form.Name.data,
            Description = form.Description.data,
            Status = "Upcoming",
            DateTime = event_datetime,
            Cost = form.Cost.data,
            Address = form.Address.data,
            AvailableTickets = form.TotalTickets.data,
            TotalTickets = form.TotalTickets.data,
            CategoryID = category.CategoryID,
            Image = db_file_path,
            Username = current_user.Username       
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

    if current_user.Username != event.Username:
        abort(404)

    if event is None:
        abort(404)
   
    form = createEditForm(event)

    if form.validate_on_submit():

        category = Category.query.filter_by(Name = form.Category.data.upper()).first()
        
        event_datetime = datetime.strptime( (str(form.Date.data) + ' ' + str(form.Time.data)) , "%Y-%m-%d %H:%M:%S")
        
        if event_datetime < datetime.now() :
            flash("You can't create an event for the past!")
            return redirect(url_for('event.edit', id = id))

        if category is None:
            category = Category(
                Name = form.Category.data.upper().replace(' ', '_')
            )

            db.session.add(category)
            db.session.commit()

        event.Name = form.Name.data
        event.CategoryID = category.CategoryID        
        event.Cost = form.Cost.data
        event.Address = form.Address.data
        event.TotalTickets = form.TotalTickets.data
        event.Description = form.Description.data

        if form.CancelEvent.data:
            event.Status = "Cancelled"

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

        return redirect(url_for('event.order', id = order.OrderID))

    return redirect(url_for('event.view', id = id))    

@eventbp.route('/order/history')
@login_required
def history():
    
    orders = current_user.Orders

    return render_template('event/history.html', orders = orders)

@eventbp.route('/order/<int:id>')
@login_required
def order(id):

    orders = current_user.Orders

    for order in orders:
        if id == order.OrderID:
            return render_template('event/order.html', order = order)

    return abort(404)

