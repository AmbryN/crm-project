from flask import Flask, request, render_template, session, redirect, url_for
from helpers import error, login_required, eur, rows2dict
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine, MetaData

# Declare the app
app = Flask(__name__)

# Define database
engine = create_engine('sqlite:///crm.db', convert_unicode=True)
metadata = MetaData(bind=engine)

# Secret key for session (TO KEEP SECRET)
app.secret_key = b'\x8e&L\x8c\xf4\xa7\xd0geS%\x1a\xe7\x9b\xb3.'

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route('/')
@login_required
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if not request.form.get("username"):
            return error("must provide an username", 400)
        elif not request.form.get("password"):
            return error("must provide a password", 400)
        else:
            username = request.form.get("username")
            password = request.form.get("password")
            rows = rows2dict(engine.execute("SELECT * FROM users WHERE username=:username", username=username))
            if check_password_hash(rows[0]["hash"], password):
                session['user_id'] = rows[0]["id"]
            else:
                return error("username or password error", 401)
            return redirect(url_for("index"))
    else:
        return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop("user_id", None)
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if not request.form.get("username"):
            return error("must provide an username", 400)
        elif not request.form.get("password"):
            return error("must provide a password", 400)
        elif not request.form.get("password") == request.form.get("confirmation"):
            return error("password and confirmation don't match", 400)
        else:
            username = request.form.get("username")
            hashed = generate_password_hash(request.form.get("password"))
            rows = engine.execute("SELECT * FROM users WHERE username = :username", username=username)
            if not rows:
                engine.execute("INSERT INTO users (username, hash) VALUES (:username, :hashed)", username=username, hashed=hashed)
            else:
                return error("username already taken", 400)
            return render_template("index.html")
    else:
        return render_template("register.html")