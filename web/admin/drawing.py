from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from models.item import Item, ItemSchema
from models.ticket import Ticket, TicketSchema
from models.user import User, UserSchema
from config import const as CONSTANTS
import logging
import random
import string
from sqlalchemy import asc

log = logging.getLogger()
web_admin_drawings = Blueprint('web_admin_drawings', __name__)

# Used in the seed generator for the random.seed() function.
def string_num_generator(size):
    chars = string.ascii_lowercase + string.digits + string.ascii_uppercase
    return ''.join(random.choice(chars) for _ in range(size))


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
    tickets = Ticket.query.filter(Ticket.item_id.in_((item.id, CONSTANTS.GLOBAL_TICKET_ID)), Ticket.active == True).all().order_by("id desc")

    return render_template('admin/drawing.html', item=item, tickets=tickets)


# Route used to perform the actual drawing for an item
@web_admin_drawings.route("<id>", methods=['POST'])
@login_required
def drawing_post_ajax(id):
    log.info("web_admin_drawings.drawing_post_ajax")
    ticket_schema = TicketSchema()
    item_schema = ItemSchema()
    user_schema = UserSchema()

    item = Item.query.get(id)
    tickets = Ticket.query.filter(Ticket.item_id.in_((item.id, CONSTANTS.GLOBAL_TICKET_ID)), Ticket.active == True).order_by(asc(Ticket.id)).all()

    # Make sure that the item is still available
    if item.available is False:
        res = {
            "success": False,
            "error_message": "Item no longer available",
        }
        return jsonify(res)

    if len(tickets) < 1:
        res = {
            "success": False,
            "error_message": "No active tickets for the item",
        }
        return jsonify(res)

    prng = string_num_generator(128)
    log.debug(f'PRNG Value: {prng}')
    
    # Set the Random Seed value
    random.seed(prng)

    #Select a Winning Ticket
    log.debug(f'Tickets: {tickets}')
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

    log.debug(f'Global Ticket Item ID: {CONSTANTS.GLOBAL_TICKET_ID}')
    log.debug(f'Winning Ticket Item ID: {winning_ticket.item_id}')
    log.debug(f'Winning Ticket ID: {winning_ticket.id}')

    # # Ensure Global Tickets remain active for additional drawings. 
    # if winning_ticket.item_id == CONSTANTS.GLOBAL_TICKET_ID:
    #     winning_ticket.active = True
    #     winning_ticket.update()

    res = {
        "winning_user": user_schema.dump(winning_user),
        "winning_ticket": ticket_schema.dump(winning_ticket),
        "item": item_schema.dump(item),
        "stats": {
            "total_tickets": len(tickets),
            "tickets_purchased": winning_user_tickets_purchased
        }
    }

    return jsonify(res)
