import os

from flask import flask, flash, redirect, render_template, request, session
from flask_session import session
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, euro