from flask import Blueprint, render_template, redirect, request, jsonify, url_for
from flask_login import login_required, current_user
from models.item import Item
from models.order import Order
from config import const as CONSTANTS
from services import square_service
import logging
import uuid
import requests
import json

log = logging.getLogger()
web_checkout = Blueprint('web_checkout', __name__)


# context_processor used for loading global blueprint variables
@web_checkout.context_processor
def inject_globals():
    return dict(user=current_user)


# Route used to start the checkout process with our 3rd party payment processor
@web_checkout.route("/start", methods=['POST'])
@login_required
def start_checkout():
    log.info("web_checkout.start_checkout")

    # Get our shopping cart data from the request
    body = request.get_json()
    cart = body.get('cart')

    res = square_service.create_transaction(cart, current_user)

    if res['success'] is not True:
        return jsonify({
            "success": False,
            "errors": res['errors']
        }), 200
    else:
        return jsonify({
            "success": True,
            "checkout_url": res['checkout_url']
        }), 200


# Route used to complete the checkout process
@web_checkout.route("/complete", methods=['GET'])
def complete_checkout():
    log.info("web_checkout.complete_checkout")

    checkout_id = request.args.get('checkoutId', None)
    transaction_id = request.args.get('transactionId', None)

    # Create a new order record
    order = Order()
    order.square_checkout_id = checkout_id
    order.square_transaction_id = transaction_id
    order.payment_status = 'PENDING'
    order.update()

    # Redirect the user back to the home page
    return redirect(url_for('web_items.items_get', checkout_complete=True))
