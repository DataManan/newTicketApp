from flask import Blueprint, render_template, url_for, redirect, current_app
from . import db
from flask_admin import Admin
from flask_wtf import FlaskForm

admin_controls = Blueprint('admin_controllers', __name__)

@admin_controls.route("/venue_mgmt")
def venues():
    return render_template("venuemgmt.html.jinja2")