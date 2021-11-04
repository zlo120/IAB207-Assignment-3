from flask import Blueprint, render_template
from threading import current_thread
from flask import Blueprint, abort
from flask_login import current_user
from flask.helpers import url_for
from flask_login.utils import login_required
from werkzeug.utils import redirect, secure_filename
import os
from datetime import datetime

from website.auth import login

from . import db
from .models import Event, Category, Comment, Order, User 

bp = Blueprint('main', __name__)


@bp.route('/')
def index():

    events = Event.query.all()
    categories = Category.query.all()

    return render_template("index.html", events = events, categories = categories)
