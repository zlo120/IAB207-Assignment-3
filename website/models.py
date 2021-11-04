from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "users"
    ID = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement=True)
    Username = db.Column(db.String(256), nullable = False)
    password_hash = db.Column(db.String(255), nullable = False)
    Name = db.Column(db.String(256), nullable = False)
    Email = db.Column(db.String(256), nullable = False)
    ContactNum = db.Column(db.Integer, nullable = True)
    address = db.Column(db.String(100), index = True, nullable = False)

    # Foreign keys : Comment, Orders, Events?
    Orders = db.relationship("Order", backref="User")
    Comments = db.relationship("Comment", backref="User")

    def get_id(self):
        return self.ID

class Order(db.Model):
    __tablename__ = "orders"
    OrderID = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement=True)
    NumTickets = db.Column(db.Integer, nullable = False)

    # Foreign keys : Event, User
    EventID = db.Column(db.Integer, db.ForeignKey('events.EventID'))
    Username = db.Column(db.Integer, db.ForeignKey('users.Username'))

class Comment(db.Model):
    __tablename__ = "comments"
    CommentID = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement=True)
    Comment = db.Column(db.String(256), nullable = False)
    DateTime = db.Column(db.DateTime, default=datetime.now())
    
    # Foreign keys : User, Event
    Username = db.Column(db.Integer, db.ForeignKey('users.Username'))
    EventID = db.Column(db.Integer, db.ForeignKey('events.EventID'))

class Event(db.Model):
    __tablename__ = "events"
    EventID = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement=True)
    Name = db.Column(db.String(256), nullable = False)
    Description = db.Column(db.String(256), nullable = False)
    Status = db.Column(db.String(256), nullable = False)
    DateTime = db.Column(db.DateTime, nullable = False)
    Cost = db.Column(db.Integer, nullable = False)
    Address = db.Column(db.String(256), nullable = False) 

    AvailableTickets = db.Column(db.Integer, nullable = False)
    TotalTickets = db.Column(db.Integer, nullable = False)

    # Image file location
    Image = db.Column(db.String(256), nullable = True)

    # Foreign keys : User, Category
    Username = db.Column(db.Integer, db.ForeignKey('users.Username'))
    CategoryID = db.Column(db.Integer, db.ForeignKey('categories.CategoryID'))

    Comments = db.relationship("Comment", backref="Event")
    Orders = db.relationship("Order", backref="Event")
    
class Category(db.Model):
    __tablename__ = "categories"
    CategoryID = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement=True)
    Name = db.Column(db.String(256), nullable = False)

    Events = db.relationship("Event", backref="Category")