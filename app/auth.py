from flask import Blueprint, render_template, flash, redirect, url_for, jsonify, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, ValidationError
from wtforms.validators import InputRequired, Email, Length
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from .forms import SignupForm


auth = Blueprint('auth', __name__)
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LoginForm(FlaskForm):
    username = StringField('username', validators=[
                           InputRequired(), Length(min=4, max=16)])
    password = PasswordField('password', validators=[
                             InputRequired(), Length(min=8, max=150)])
    remember = BooleanField('remember me')

    # def validate_password(self, field):
    #   user = User.query.filter_by(username=self.username.data).first()
    #    if user is None:
    #         raise ValidationError('Invalid username or password')
    #     if check_password_hash(user.password, field.data):
    #         raise ValidationError('Invalid username or password')


class RegistrationForm(FlaskForm):

    first_name = StringField('first name', validators=[
                             InputRequired(), Length(min=4, max=16)])

    last_name = StringField('last name', validators=[
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
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('controllers.index', current_user=current_user))

        return "<h1> Login values are invalid </h1>"
    # else:
    #     flash('user dosen\'t exists', category='error')
    #     # return redirect(url_for('auth.user_login'))

    return render_template("login_page.html.jinja2", form=form)
    # return "<h1> Login values are invalid </h1>"


@auth.route("/signup", methods=['GET', 'POST'])
def user_signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        # create a new user
        hashed_password = generate_password_hash(
            form.password.data, method='sha256')
        user = User(email=form.email.data,
                    password=hashed_password,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    username=form.username.data)
        # add the new user to the database
        db.session.add(user)
        db.session.commit()
        flash('You have successfully signed up!', 'success')
        return redirect(url_for('auth.user_login'))
    return render_template("signup_page.html.jinja2", form=form)


@auth.route('/success')
@login_required
def success():
    return render_template('showsuccess.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    # session['logged_in']=False
    return redirect(url_for('controllers.index'))
