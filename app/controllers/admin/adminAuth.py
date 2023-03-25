# from crypt import methods
# from sys import prefix
# from flask import Blueprint, render_template, flash, redirect, url_for, jsonify
# from .models import User
# from . import db
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import LoginManager, login_user as login_admin, login_required, logout_user as logout_admin, current_user as current_admin
# from .admin_forms import AdminLoginForm

# admin_auth = Blueprint('adminAuth', __name__, url_prefix='/admin')
# # admin_login_manager = LoginManager()


# # @admin_login_manager.user_loader
# # def load_admin(admin_id):
# #     return Admin.query.get_or_404(int(admin_id))

# @admin_auth.route("/login", methods=['GET', 'POST'])
# def admin_login():
#     form = AdminLoginForm()
#     if form.validate_on_submit():
#         admin = User.query.filter_by(username=form.username.data).first()
#         if admin and admin.isadmin:
#             if form.password.data == admin.password:
#                 login_admin(admin, remember=form.remember.data)
#                 return redirect(url_for('admin_controllers.adminhome', current_user=current_admin, admin_id=admin.admin_id))
            
#         flash("invalid admin credentials", category='error')
#         return redirect(url_for('admin_auth.admin_login'))
    
#     return render_template('admin_login_form.html.jinja2', form=form)


# @admin_auth.route('/logout')
# @login_required
# def logout():
#     logout_admin()
    
#     return redirect(url_for('controllers.index'))
