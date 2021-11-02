
from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField, PasswordField, IntegerField, FloatField, TextAreaField
from wtforms.fields.html5 import DateField, TimeField
from wtforms.validators import InputRequired, Email, EqualTo, Optional, Length, NumberRange
from flask_wtf.file import FileField, FileRequired, FileAllowed

from datetime import datetime

#creates the login information
class LoginForm(FlaskForm):
    user_name = StringField("Username", validators=[InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[InputRequired('Enter a password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired("Please enter your name")])
    user_name=StringField("Username", validators=[InputRequired("Please enter a username")])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    contact_number = IntegerField("Contact Number", validators=[NumberRange(min=0, max=9999999999, message="Please enter a valid phone number")])
    address = StringField("Address", validators=[InputRequired()])
    
    #add buyer/seller - check if it is a buyer or seller hint : Use RequiredIf field


    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired("Please enter a password"),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    #submit button
    submit = SubmitField("Register")

# EVENT FORMS

ALLOWED_FILE = ['.PNG','.png',".jpg",'.JPG','.jpeg','.jpeg']


class CreateEvent(FlaskForm):
    Name = StringField("Name", validators=[InputRequired()])
    Description = TextAreaField("Description", validators=[InputRequired()])
    Date = DateField("Date", validators=[InputRequired()])
    Time = TimeField("Time", validators=[InputRequired()])
    Cost = IntegerField("Cost", validators=[InputRequired()])
    Address = StringField("Address", validators=[InputRequired()])
    TotalTickets = IntegerField("Total number of tickets", validators=[InputRequired()])
    
    Category = StringField("Category", validators=[InputRequired()])

    CoverImage = FileField('Image', validators=[ FileRequired(message='Image cannot be empty'),  FileAllowed( ['PNG','png',"jpg",'JPG','jpeg','JPEG'] , message='Only supports jpg, jpeg and png!')])
    
    Create = SubmitField("Create")

def createEditForm(event):

    class EditForm(FlaskForm):
        Name = StringField("Name", validators=[Optional()], render_kw={"value":event.Name})
        Description = TextAreaField("Description", validators=[Optional()], render_kw={"value":event.Name})
        Date = DateField("Date", validators=[Optional()])
        Time = TimeField("Time", validators=[Optional()])
        Cost = IntegerField("Cost", validators=[Optional()], render_kw={"value":event.Cost})
        Address = StringField("Address", validators=[Optional()], render_kw={"value":event.Address})
        TotalTickets = IntegerField("Total number of tickets", validators=[Optional()], render_kw={"value":event.TotalTickets})
        
        Category = StringField("Category", validators=[Optional()], render_kw={"value":event.Category.Name})
        
        Create = SubmitField("Create")
    
    return EditForm()

def bookEvent(event):
    # Booking form
    class CreateBooking(FlaskForm):
        Amount = IntegerField("Number of Tickets", validators=[InputRequired(), NumberRange(min = 1, max = event.AvailableTickets)])
        Submit = SubmitField("Place order")

    return CreateBooking()

# Comment form
class CreateComment(FlaskForm):
    Content = StringField("Comment", validators=[InputRequired()])
    Submit = SubmitField("Post")