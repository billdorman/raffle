from flask import Blueprint, request, render_template, url_for, redirect
from flask_login import login_required, current_user
from models.user import UserSchema
import logging


log = logging.getLogger()
web_search = Blueprint('web_search', __name__)


# context_processor used for loading global blueprint variables
@web_search.context_processor
def inject_globals():
    return dict(user=current_user)


# Route used to display the search page
@web_search.route("/search", methods=['GET'])
@login_required
def search_get():
    log.info("web_search.search_get")

    return render_template('items.html')


# Route used to handle posts from the search form
@web_search.route("/search", methods=['POST'])
@login_required
def search_post():
    log.info("web_search.search_post")
    user_schema = UserSchema()

    search_phrase = request.form.get('search')

    return redirect(url_for('web_search.search_get'))
