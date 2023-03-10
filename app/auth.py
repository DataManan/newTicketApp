# from wsgiref.validate import validator
from hashlib import sha256
from flask import Blueprint, render_template, flash, redirect, url_for
import flask_login
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

# login manager
# login_manager = LoginManager()
# login_manager = 
class LoginForm(FlaskForm):
    username = StringField('username', validators=[
                           InputRequired(), Length(min=4, max=16)])
    password = PasswordField('password', validators=[
                             InputRequired(), Length(min=8, max=150)])
    remember = BooleanField('remember me')


class RegistrationForm(FlaskForm):
    first_name = StringField('first_name', validators=[
                             InputRequired(), Length(min=4, max=16)])
    last_name = StringField('last_name', validators=[
                            InputRequired(), Length(min=4, max=16)])
    username = StringField('username', validators=[
                           InputRequired(), Length(min=4, max=16)])
    email = StringField('email', validators=[InputRequired(), Email(
        message='Invalid Email'), Length(max=80)])
    password = PasswordField('password', validators=[
                             InputRequired(), Length(min=8, max=80)])


@auth.route("/login", methods=['GET', 'POST'])
def user_login():
    form = LoginForm()

    if form.validate_on_submit():
        # return "<h1> Already Logged In " + " " + form.username.data + " " + "</h1>"
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                flash('Logged in successfully', category='success')
                login_user(user, remember=form.remember.data)
                return redirect(url_for('auth.success'))
            else:
                flash('wrong password', category='error')
        else:
            flash('user dosen\'t exists')

    return render_template("login_page.html.jinja2", form=form)


@auth.route("/signup", methods=['GET', 'POST'])
def user_signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        # return "<h1> Already Logged In " + " " +form.email.data + " "+ form.username.data + " " + "</h1>"
        password_hash = generate_password_hash(
            form.password.data, method='sha256')
        new_user = User(
            email=form.email.data,
            password=password_hash,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('controllers.index'))
    return render_template("signup_page.html.jinja2", form=form)


@auth.route('/success')
@login_required
def success():
    return render_template('showsuccess.html')
