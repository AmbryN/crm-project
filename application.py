from flask import Flask, request, render_template, session, redirect, url_for
from helpers import error, login_required, eur

# Declare the app
app = Flask(__name__)

# Secret key for session (TO KEEP SECRET)
app.secret_key = b'\x8e&L\x8c\xf4\xa7\xd0geS%\x1a\xe7\x9b\xb3.'

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if not request.form.get("username"):
            return error("must provide an username", 400)
        if not request.form.get("password"):
            return error("must provide a passowrd", 400)

        # TODO : DB query for user and check password
        #rows = db
        #session['user_id'] = rows[0]["id"]
        logging.info('User logged in')
        return redirect(url_for("index"))
    else:
        return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))