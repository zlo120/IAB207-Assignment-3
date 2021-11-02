from flask import Blueprint, flash, render_template, request, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.validators import Email
from .models import User
from .forms import LoginForm, RegisterForm
from flask_login import login_user, login_required, logout_user
from . import db


#create a blueprint
bp = Blueprint('auth', __name__)


# this is the hint for a login function
@bp.route('/login', methods=['GET', 'POST'])
def login(): #view function
    login_form = LoginForm()
    error = None
    if(login_form.validate_on_submit() == True):
        user_name = login_form.user_name.data
        password = login_form.password.data
        u1 = User.query.filter_by(Username = user_name).first()
        if u1 is None:
            error = 'Incorrect user name'
        elif not check_password_hash(u1.password_hash, password): # takes the hash and password
            error = 'Incorrect password'
        if error is None:
            login_user(u1)
            flash("You are succesfully logged in!")
            return redirect(url_for('main.index'))
        else:
            flash(error)
            return redirect(url_for('auth.login'))

    return render_template('user/login.html', form = login_form, heading = 'Login')

@bp.route('/register', methods = ['GET', 'POST'])
def register():
    register = RegisterForm()
    if register.validate_on_submit():
        name = register.name.data
        uname = register.user_name.data
        email = register.email_id.data
        number = register.contact_number.data
        address = register.address.data
        pwd = register.password.data
        u1 = User.query.filter_by(Username = uname).first()
        if u1:
            flash('An account with that username already exists')
            return redirect(url_for('auth.register'))
        pwd_hash = generate_password_hash(pwd)
        new_user = User(Name = name, Username = uname, Email = email, ContactNum = number, address = address, password_hash = pwd_hash)
        db.session.add(new_user)
        db.session.commit()
        return redirect (url_for('main.index'))
    else:
        return render_template('user/register.html', form = register, heading = 'Register')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You are now logged out")
    return redirect(url_for('main.index'))