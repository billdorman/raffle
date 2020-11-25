from flask import Blueprint, render_template, redirect, request
from flask_login import login_required, current_user
from models.item import Item
from models.item_image import ItemImage
from models.ticket import Ticket
from config import const as CONSTANTS
import logging
import boto3

log = logging.getLogger()
web_items = Blueprint('web_items', __name__)


# context_processor used for loading global blueprint variables
@web_items.context_processor
def inject_globals():
    return dict(user=current_user)


# Route used to display the items page
@web_items.route("", methods=['GET'])
@login_required
def items_get():
    log.info("web_items.items_get")

    category = request.args.get('category', None)

    query = Item.query.filter_by(available=True, category=category) if category is not None else Item.query.filter_by(available=True)

    items = query.all()

    tickets = Ticket.query.filter_by(user_id=current_user.id, active=True).all()

    # Build a dictionary to store the number of tickets purchased for each item by the current user
    item_tickets = {}
    for item in items:
        item_tickets[item.id] = sum(map(lambda ticket : ticket.item_id == item.id, tickets))

    return render_template('items.html', items=items, item_tickets=item_tickets, categories=CONSTANTS.ITEM_CATEGORIES)
