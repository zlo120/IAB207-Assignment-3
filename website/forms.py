
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField
from wtforms.fields.html5 import DateField, TimeField
from wtforms.fields.core import IntegerField
from wtforms.validators import InputRequired, Length, Email, EqualTo, Optional
from wtforms.widgets.core import Input

from datetime import datetime


#creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    
    #add buyer/seller - check if it is a buyer or seller hint : Use RequiredIf field


    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    #submit button
    submit = SubmitField("Register")

# EVENT FORMS

class CreateEvent(FlaskForm):
    Name = StringField("Name", validators=[InputRequired()])
    Date = DateField("Date", validators=[InputRequired()])
    Time = TimeField("Date", validators=[InputRequired()])
    Cost = IntegerField("Cost", validators=[InputRequired()])
    Address = StringField("Address", validators=[InputRequired()])
    TotalTickets = IntegerField("Total number of tickets", validators=[InputRequired()])
    
    Category = StringField("Category", validators=[InputRequired()])
    
    Create = SubmitField("Create")

def createEditForm(event):

    class EditForm(FlaskForm):
        Name = StringField("Name", validators=[Optional()], render_kw={"value":event.Name})
        Date = DateField("Date", validators=[Optional()])
        Time = TimeField("Date", validators=[Optional()])
        Cost = IntegerField("Cost", validators=[Optional()], render_kw={"value":event.Cost})
        Address = StringField("Address", validators=[Optional()], render_kw={"value":event.Address})
        TotalTickets = IntegerField("Total number of tickets", validators=[Optional()], render_kw={"value":event.TotalTickets})
        
        Category = StringField("Category", validators=[Optional()], render_kw={"value":event.Category.Name})
        
        Create = SubmitField("Create")
    
    return EditForm()