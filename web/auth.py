from flask import Blueprint, request, render_template, flash, url_for, redirect
from flask_login import login_user, logout_user
from marshmallow.validate import ValidationError
from models.user import User, UserSchema
from services.auth_service import sign_in
from services.crypt_service import pwd_context
import logging
from services.email_service import send_email

log = logging.getLogger()
web_auth = Blueprint('web_auth', __name__)


message_subject = 'Your new SweenyPTO.org Account'
message_body = '{first_name}, thank you for registering your new account. Your login name will be {email}.'

# Route used to display the login page
@web_auth.route("/login", methods=['GET'])
def login_get():
    log.info("web_auth.login_get")

    return render_template('login.html')


# Route used for authenticating user credentials and logging them into the site
@web_auth.route("/login", methods=['POST'])
def login_post():
    log.info("web_auth.login_post")
    user_schema = UserSchema()

    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # Attempt to log the user in using the passed in credentials
    current_user = sign_in(email, password)

    if not current_user:
        flash('Invalid username or password', 'danger')
        return redirect(url_for('web_auth.login_get'))

    # Valid user, use flask_login to log the user in and redirect to index
    login_user(current_user, remember)
    return redirect(url_for('web_items.items_get'))


# Route used for logging the user out
@web_auth.route("/logout", methods=['GET'])
def logout():
    log.info("web_auth.logout")
    logout_user()
    return redirect(url_for('web_auth.login_get'))


# Route used to display the register page
@web_auth.route("/register", methods=['GET'])
def register_get():
    log.info("web_auth.register_get")

    return render_template('register.html')


# Route used for registering a new user account
@web_auth.route("/register", methods=['POST'])
def register_post():
    log.info("web_auth.register_post")
    user_schema = UserSchema()

    password = pwd_context.hash(request.form.get('password', ''))

    user_data = {
        "first_name": request.form.get('first_name', None),
        "last_name": request.form.get('last_name', None),
        "email": request.form.get('email', None),
        "password": password,
        "address": request.form.get('address', None),
        "city": request.form.get('city', None),
        "state": request.form.get('state', None),
        "zip": request.form.get('zip', None)
    }

    # Check that the email address isn't already in use
    existing_user = User.query.filter_by(email=user_data['email']).first()
    if existing_user:
        flash('Email address already in use', 'danger')
        return redirect(url_for('web_auth.register_get'))

    # Attempt to create a user with the passed in details
    try:
        user = user_schema.load(user_data)
        user.active = True
        user.update()
        send_email(user)
    except ValidationError as ex:
        return '', 400

      # Valid user, use flask_login to log the user in and redirect to the home page
    login_user(user, True)
    return redirect(url_for('web_items.items_get'))
    
    email_service.send_email(email, message_subject, message_body)