from flask import Blueprint, render_template, flash, redirect, url_for, jsonify
from ..models.models import User
from .. import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from .users.forms import LoginForm, RegistrationForm, AdminLoginForm
from functools import wraps
import datetime
auth = Blueprint('auth', __name__)
login_manager = LoginManager()

"""this is a decorator function to make sure that the person, entering the routes is an admin

    Returns:
        decorator: _description_
    """


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        is_admin = False
        if current_user.is_authenticated:
            is_admin = current_user.isadmin

        if not is_admin:
            # If a user who is not an admin tries to access admin pages he/she will get a error
            # message that the route doesn't exits, but if the admin tries to access the page it opens
            
            return "<h1>Routes doesn't exits</h1>", 400
        elif is_admin:
            return f(*args, **kwargs)

    return decorated

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


duration = datetime.timedelta(minutes=30)

@auth.route("/login", methods=['GET', 'POST'])
def user_login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user :
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)

                return redirect(url_for('controllers.index'))
        
            
        flash('user dosen\'t exists', category='error')
        return redirect(url_for('auth.user_login'))
    

    return render_template("user/login_n_signup/login_page.html.jinja2", form=form)
    # return "<h1> Login values are invalid </h1>"

@auth.route("/admin_login", methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.isadmin:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data, duration=duration)
                return redirect(url_for('admin_controllers.adminhome'))
            
    return render_template('admin/admin_login_form.html.jinja2', form=form)


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
    return render_template("user/login_n_signup/signup_page.html.jinja2", form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    # session['logged_in']=False
    return redirect(url_for('controllers.index'))


@auth.route('/admin/logout')
def admin_logout():
    logout_user()
    return redirect(url_for('controllers.index'))
