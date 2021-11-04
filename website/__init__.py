#import flask - from the package import class
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db=SQLAlchemy()
login_manager = LoginManager()

#create a function that creates a web application
# a web server will run this web application
def create_app():
  
    app=Flask(__name__)  # this is the name of the module/package that is calling this app
    app.debug=True
    app.secret_key='utroutoru'
    #set the app configuration data 
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///sitedata.sqlite'
    #initialize db with flask app
    db.init_app(app)

    from .models import User, Order, Comment, Event, Category

    bootstrap = Bootstrap(app)
    
    #initialize the login manager
    login_manager.init_app(app)
    
    #set the name of the login function that lets user login
    # in our case it is auth.login (blueprintname.viewfunction name)
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    #create a user loader function takes userid and returns User
    from .models import User  # importing here to avoid circular references
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    #config upload folder
    UPLOAD_FOLDER = '/static/events'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    #importing views module here to avoid circular references
    # a commonly used practice.
    from . import views
    app.register_blueprint(views.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import event
    app.register_blueprint(event.eventbp)

    @app.errorhandler(400)
    def bad_request(e):
        return render_template("error_handlers/400.html")
        
    @app.errorhandler(401)
    def not_authenticated(e):
        return render_template("error_handlers/401.html")
        
    @app.errorhandler(403)
    def unauthorised(e):
        return render_template("error_handlers/403.html")
        
    @app.errorhandler(404)
    def not_found(e):
        return render_template("error_handlers/404.html")
        
    @app.errorhandler(500)
    def internal_error(e):
        return render_template("error_handlers/500.html")

    app.register_error_handler(400, bad_request)
    app.register_error_handler(401, not_authenticated)
    app.register_error_handler(403, unauthorised)
    app.register_error_handler(404, not_found)
    app.register_error_handler(500, internal_error)

    
    return app