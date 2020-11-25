from flask import Blueprint, render_template, redirect, request
from flask_login import login_required, current_user
from models.item import Item
from models.item_image import ItemImage
from models.ticket import Ticket
from config import const as CONSTANTS
import logging
import boto3

log = logging.getLogger()
web_drawing = Blueprint('web_drawing', __name__)

@web_drawing.context_processor
def inject_globals():
    return dict(user=current_user)

# Route used to initiate a drawing for an item.
@web_drawing.route("<item_id>", methods=["GET"])
@login_required
def ticket_get(item_id):
    log.info(f"{user} access the drawing page.")