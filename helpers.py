from flask import redirect, render_template, request, session, url_for
from functools import wraps

def error(message, code=400):
    """Render message as an apology to user."""
    return render_template("error.html", message=message, code=code), code

def login_required(f):
    """
    Decorate routes to require login.
    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def eur(value):
    """Format a value as EUR."""
    return f"{value:,.2f}€"