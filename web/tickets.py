from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import desc
from models.ticket import Ticket
from config import const as CONSTANTS
import logging

log = logging.getLogger()
web_tickets = Blueprint('web_tickets', __name__)


# context_processor used for loading global blueprint variables
@web_tickets.context_processor
def inject_globals():
    return dict(user=current_user)


# Route used to display the ticket list page
@web_tickets.route("", methods=['GET'])
@login_required
def tickets_get():
    log.info("web_tickets.tickets_get")

    tickets = Ticket.query.filter_by(user_id=current_user.id).order_by(desc(Ticket.item_id)).all()

    return render_template('tickets.html', tickets=tickets)
