from flask import render_template
from flask import app


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404
    
@app.errorhandler(403)
def not_found_error(error):
    return render_template('403.html'), 403

@app.errorhandler(402)
def internal_error(error):
    return render_template('402.html'), 402

@app.errorhandler(401)
def internal_error(error):
    return render_template('401.html'), 401
    
@app.errorhandler(400)
def internal_error(error):
    return render_template('400.html'), 400

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500