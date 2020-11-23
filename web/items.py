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

    return render_template('items.html', items=items, item_tickets=item_tickets)


# Route used to display an image by creating an S3 presigned url
@web_items.route("/<item_id>/images/<image_id>", methods=['GET'])
@login_required
def item_image_view(item_id, image_id):
    log.info("web_items.item_image_view")
    image = ItemImage.query.get(image_id)

    # Build a signed S3 url for viewing the image and redirect to it
    client = boto3.client('s3',
                          region_name='us-east-1',
                          aws_access_key_id=CONSTANTS.S3_ACCESS_KEY,
                          aws_secret_access_key=CONSTANTS.S3_SECRET_KEY)

    uri = client.generate_presigned_url('get_object',
                                        Params={'Bucket': image.s3_bucket_name, 'Key': image.s3_bucket_path},
                                        ExpiresIn=CONSTANTS.S3_URL_EXPIRATION_TIME)
    return redirect(uri, 302)
