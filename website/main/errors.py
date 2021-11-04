from flask import render_template
from . import app

@app.errorhandler(404)
def page_not_found(e):
    return render_template("error_handlers/404.html")

@app.errorhandler(401)
def not_authenticated(e):
    return render_template("error_handlers/401.html")