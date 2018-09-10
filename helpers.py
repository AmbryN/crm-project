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
    return f"{value} €"
    

def rows2dict(rows):
    """Converts the ResultProxy from SQLAlchemy to a dict
    https://stackoverflow.com/questions/1958219/convert-sqlalchemy-row-object-to-python-dict
    """
    l = []
    for row in rows:
        row_as_dict = dict(row)
        l.append(row_as_dict)
    return l

def row2dict(rows):
    """Converts the ResultProxy from SQLAlchemy to a dict
    when only one row is returned
    https://stackoverflow.com/questions/1958219/convert-sqlalchemy-row-object-to-python-dict
    """
    l = []
    for row in rows:
        row_as_dict = dict(row)
        l.append(row_as_dict)
    return l[0]