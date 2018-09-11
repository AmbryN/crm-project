import os

from flask import Flask, request, render_template, session, redirect, url_for, jsonify
from helpers import error, login_required, eur, rows2dict, row2dict
from math import trunc
from sqlalchemy import create_engine, MetaData
from werkzeug.security import generate_password_hash, check_password_hash

# Declare the app
app = Flask(__name__)

# Define database
engine = create_engine('sqlite:///crm.db', convert_unicode=True)
metadata = MetaData(bind=engine)

# Secret key for session
SECRET_KEY = os.environ.get("SECRET_KEY", "")
app.secret_key = SECRET_KEY

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filters
app.jinja_env.filters['eur'] = eur

# Overview's route
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    # Base case, show open projects
    filt = "open"
    if request.method == 'POST':
        filt = request.form.get("filter")
        if filt == "open":
            return redirect(url_for('index'))
        elif filt == "offered":
            # Get all the projects with status offered
            rows = rows2dict(engine.execute("""SELECT p.id AS id, c.name AS client, p.topic AS topic, p.open_date AS open_date, p.offer_date, p.offer_price, s.name AS status
                                            FROM projects p 
                                            INNER JOIN clients c ON p.client_id = c.id 
                                            INNER JOIN status s ON p.status_id = s.id
                                            WHERE status = "offered"
                                            ORDER BY offer_date"""))
        elif filt == "ordered":
            # Get all the projects with status ordered
            rows = rows2dict(engine.execute("""SELECT p.id AS id, c.name AS client, p.topic AS topic, p.open_date AS open_date, p.offer_date, p.offer_price, s.name AS status
                                            FROM projects p 
                                            INNER JOIN clients c ON p.client_id = c.id 
                                            INNER JOIN status s ON p.status_id = s.id
                                            WHERE status = "ordered"
                                            ORDER BY offer_date"""))
        elif filt == "cancelled":
            # Get all the projects with status ordered
            rows = rows2dict(engine.execute("""SELECT p.id AS id, c.name AS client, p.topic AS topic, p.open_date AS open_date, s.name AS status
                                            FROM projects p 
                                            INNER JOIN clients c ON p.client_id = c.id 
                                            INNER JOIN status s ON p.status_id = s.id
                                            WHERE status = "cancelled"
                                            ORDER BY open_date"""))
    else:
        # Get all the projects with status open
        rows = rows2dict(engine.execute("""SELECT p.id AS id, c.name AS client, p.topic AS topic, p.open_date AS open_date, p.due_date AS due_date, s.name AS status
                                        FROM projects p 
                                        INNER JOIN clients c ON p.client_id = c.id 
                                        INNER JOIN status s ON p.status_id = s.id
                                        WHERE status = "open"
                                        ORDER BY due_date"""))
    return render_template("index.html", projects=rows, filter=filt)

# Route to add a new project
@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        if not request.form.get("client"):
            return error("must provide a client", 400)
        elif not request.form.get("topic"):
            return error("must provide a topic", 400)
        elif not request.form.get("due_date"):
            return error("must select a due date", 400)
        else:
            engine.execute("INSERT INTO projects (id, client_id, topic, due_date) VALUES (NULL, :client, :topic, :due_date)",
                           client=request.form.get("client"),
                           topic=request.form.get("topic"),
                           due_date=request.form.get("due_date"))
            return redirect(url_for('index'))
    else:
        rows = rows2dict(engine.execute("SELECT * FROM clients"))
        return render_template("add.html", clients=rows)

# Route to add a new client
@app.route('/client', methods=['GET', 'POST'])
@login_required
def client():
    if request.method == 'POST':
        if not request.form.get("name"):
            return error("must provide a name for client", 400)
        else:
            # Check if client already exists
            rows = rows2dict(engine.execute("SELECT * FROM clients WHERE name = :name", name=request.form.get("name")))
            if rows:
                return error("client already exists", 400)
            else:
                engine.execute("INSERT INTO clients (name) VALUES (:name)",
                               name=request.form.get("name"))
            return redirect(url_for('index'))
    else:
        return render_template("client.html")

# Route to edit a project
@app.route('/edit/<project_id>', methods=['GET', 'POST'])
@login_required
def edit(project_id):
    if request.method == 'POST':
        if not request.form.get("client_id"):
            return error("must provide a client", 400)
        elif not request.form.get("topic"):
            return error("must provide a topic", 400)
        elif not request.form.get("due_date"):
            return error("must select a due date", 400)
        else:
            # Update the project with new values
            engine.execute("""UPDATE projects SET client_id=:client_id, topic=:topic, due_date=:due_date, status_id=:status_id, offer_date=:offer_date, offer_price=:offer_price 
                           WHERE id=:project_id""",
                           client_id=request.form.get("client_id"),
                           topic=request.form.get("topic"),
                           due_date=request.form.get("due_date"),
                           status_id=request.form.get("status_id"),
                           offer_date=request.form.get("offer_date"),
                           offer_price=request.form.get("offer_price"),
                           project_id=project_id)            
            return redirect(url_for('index'))
    else:
        # Get project_id's info
        rows = rows2dict(engine.execute("""SELECT p.id AS id, c.name AS client, p.topic AS topic, p.open_date AS open_date, p.due_date AS due_date, s.name AS status, s.id AS status_id, p.offer_date, p.offer_price
                                        FROM projects p 
                                        INNER JOIN clients c ON p.client_id = c.id 
                                        INNER JOIN status s ON p.status_id = s.id
                                        WHERE p.id = :project_id
                                        ORDER BY due_date""", project_id=project_id))
        statuses = rows2dict(engine.execute("SELECT * FROM status"))
        clients = rows2dict(engine.execute("SELECT * FROM clients"))
        return render_template('edit.html', project=rows[0], statuses=statuses, clients=clients)

# Route to login
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

# Route to logout
@app.route('/logout')
def logout():
    session.pop("user_id", None)
    return redirect(url_for('index'))

# Route for registering a new user
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

            # Check if username already exists
            rows = rows2dict(engine.execute("SELECT * FROM users WHERE username = :username", username=username))
            if not rows:
                engine.execute("INSERT INTO users (username, hash) VALUES (:username, :hashed)", username=username, hashed=hashed)
            else:
                return error("username already taken", 400)
            return redirect(url_for('index'))
    else:
        return render_template("register.html")

# Route to project statistics
@app.route('/stats', methods=['GET', 'POST'])
def stats():
    # Base case if no specific client is selected
    selected_client_id = '%'

    # If POST then a client filter has been specified
    if request.method == 'POST':
        if request.form.get("client_id") == "all":
            redirect(url_for("stats"))
        else:
            selected_client_id = request.form.get("client_id")

    # Get number of open projects
    open_projects = engine.execute("""SELECT COUNT(*) AS open_count
                                    FROM projects 
                                    WHERE status_id = 1
                                    AND client_id LIKE :selected_client_id""", selected_client_id=selected_client_id).first()
    
    # Get number of open offers
    offers = engine.execute("""SELECT COUNT(*) AS offer_count, AVG(offer_price) AS mean_offer
                            FROM projects 
                            WHERE status_id = 2
                            AND client_id LIKE :selected_client_id""", selected_client_id=selected_client_id).first()
    # Get number of orders
    orders = engine.execute("""SELECT COUNT(*) AS order_count, AVG(offer_price) AS mean_order
                            FROM projects 
                            WHERE status_id = 3
                            AND client_id LIKE :selected_client_id""", selected_client_id=selected_client_id).first()
    # Avoid division by 0
    if (offers["offer_count"] == 0):
        conversion = "N/A"
    else:
        conversion = trunc(orders["order_count"] / (offers["offer_count"] + orders["order_count"]) * 100) / 100
    
    # Create a dict with all the results
    projects = {
        "open": open_projects["open_count"],
        "offers": offers["offer_count"] + orders["order_count"],
        "mean_offer": offers["mean_offer"],
        "orders": orders["order_count"],
        "mean_order": orders["mean_order"],
        "conversion": conversion
    }
        
    clients = rows2dict(engine.execute("SELECT id, name FROM clients"))
    return render_template("stats.html", projects=projects, clients=clients, selected_client_id=selected_client_id)