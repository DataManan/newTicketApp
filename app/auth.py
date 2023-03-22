from flask import Blueprint, render_template, flash, redirect, url_for, jsonify
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from .forms import LoginForm, RegistrationForm


auth = Blueprint('auth', __name__)
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth.route("/login", methods=['GET', 'POST'])
def user_login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)

                return redirect(url_for('controllers.user_loggedin', current_user=current_user, user_id= user.user_id))
            
        flash('user dosen\'t exists', category='error')
        return redirect(url_for('auth.user_login'))
    

    return render_template("login_page.html.jinja2", form=form)
    # return "<h1> Login values are invalid </h1>"


@auth.route("/signup", methods=['GET', 'POST'])
def user_signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        # create a new user
        hashed_password = generate_password_hash(
            form.password.data, method='sha256')
        chashed_password = generate_password_hash(
            form.cpassword.data, method='sha256')
        user = User(email=form.email.data,
                    password=hashed_password,
                    cpassword = chashed_password,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    username=form.username.data)
        # add the new user to the database
        db.session.add(user)
        db.session.commit()
        flash('You have successfully signed up!', 'success')
        return redirect(url_for('auth.user_login'))
    return render_template("signup_page.html.jinja2", form=form)


@auth.route('/<user_id>/logout')
@login_required
def logout(user_id):
    logout_user()
    # session['logged_in']=False
    return redirect(url_for('controllers.index'))
