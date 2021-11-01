
from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField, PasswordField, IntegerField, TextAreaField
from wtforms.fields.html5 import DateField, TimeField
from wtforms.validators import InputRequired, Email, EqualTo, Optional
from flask_wtf.file import FileField, FileRequired, FileAllowed

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

ALLOWED_FILE = ['.PNG','.png',".jpg",'.JPG','.jpeg','.jpeg']

class CreateEvent(FlaskForm):
    Name = StringField("Name", validators=[InputRequired()])
    Description = TextAreaField("Description", validators=[InputRequired()])
    Date = DateField("Date", validators=[InputRequired()])
    Time = TimeField("Date", validators=[InputRequired()])
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
        Time = TimeField("Date", validators=[Optional()])
        Cost = IntegerField("Cost", validators=[Optional()], render_kw={"value":event.Cost})
        Address = StringField("Address", validators=[Optional()], render_kw={"value":event.Address})
        TotalTickets = IntegerField("Total number of tickets", validators=[Optional()], render_kw={"value":event.TotalTickets})
        
        Category = StringField("Category", validators=[Optional()], render_kw={"value":event.Category.Name})
        
        Create = SubmitField("Create")
    
    return EditForm()

# Comment form
class CreateComment(FlaskForm):
    Content = StringField("Comment", validators=[InputRequired()])
    Submit = SubmitField("Post")