from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskapp import db, bcrypt
from flaskapp.models import User
from flaskapp.users.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm
from flaskapp.users.utils import send_reset_email
from flask import current_app

users = Blueprint('users', __name__)     

@users.route('/register', methods=["GET", "POST"])
def register():  
    if current_user.is_authenticated:
        return redirect(url_for('main.size_input'))
    form = RegistrationForm()
    if form.validate_on_submit( ):
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, history = '')
        db.session.add(user) 
        db.session.commit() 
        flash(f'Account created for {form.username.data}!', 'success')
        current_app.logger.info('New user registered: %s', form.username.data)
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route("/login", methods=['GET', 'POST'])
def login(): 
    if current_user.is_authenticated:
        return redirect(url_for('main.size_input'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            current_app.logger.info('User login successful: %s', form.email.data)
            return redirect(next_page) if next_page else redirect(url_for('main.size_input'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            current_app.logger.warning('Invalid login attempt: %s', form.email.data)
    return render_template('login.html', title='Login', form=form)

@users.route("/logout") 
def logout():
    current_app.logger.info('User %s logged out', current_user.username)
    logout_user()
    return redirect(url_for('users.login'))  


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.size_input'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        current_app.logger.info('Password reset requested for: %s', form.email.data)
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.size_input'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        current_app.logger.warning('Invalid or expired reset token used')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        current_app.logger.warning('User %s has updated password', current_user.email)
        flash('Your password has been updated', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form) 

  