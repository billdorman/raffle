from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.item import Item
from models.ticket import Ticket
from models.user import User
from config import const as CONSTANTS
import logging
import random

log = logging.getLogger()
web_admin_drawings = Blueprint('web_admin_drawings', __name__)


# context_processor used for loading global blueprint variables
@web_admin_drawings.context_processor
def inject_globals():
    return dict(user=current_user)


# Route used to display the drawing page
@web_admin_drawings.route("<id>", methods=['GET'])
@login_required
def drawing_get(id):
    log.info("web_admin_drawings.drawing_get")
    item = Item.query.get(id)
    tickets = Ticket.query.filter(Ticket.item_id.in_((item.id, CONSTANTS.GLOBAL_TICKET_ID)), Ticket.active == True).all()

    return render_template('admin/drawing.html', item=item, tickets=tickets)


# Route used to perform the actual drawing for an item
@web_admin_drawings.route("<id>", methods=['POST'])
@login_required
def drawing_post(id):
    log.info("web_admin_drawings.drawing_post")
    item = Item.query.get(id)
    tickets = Ticket.query.filter(Ticket.item_id.in_((item.id, CONSTANTS.GLOBAL_TICKET_ID)), Ticket.active == True).all()

    # Make sure that the item is still available
    if item.available is False:
        return render_template('admin/drawing-unavailable.html', item=item)

    if len(tickets) < 1:
        return render_template('admin/drawing-empty.html', item=item)

    winning_ticket = random.choice(tickets)

    winning_user = User.query.get(winning_ticket.user_id)

    winning_user_tickets_purchased = sum(1 for t in tickets if t.user_id == winning_user.id)

    # Mark the item as being unavailable
    item.available = False
    item.update()

    # Mark the winning ticket as inactive
    winning_ticket.active = False
    winning_ticket.is_winner = True
    winning_ticket.update()


    return render_template('admin/drawing-winner.html',
                           item=item,
                           winning_ticket=winning_ticket,
                           winning_user=winning_user,
                           total_tickets=len(tickets),
                           tickets_purchased=winning_user_tickets_purchased)