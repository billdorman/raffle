from flask import url_for
from config import const as CONSTANTS
from models.order import Order
from models.item import Item
import requests
import json
import uuid


def create_transaction(cart, user):
    # Get more details from the database for each item id
    item_ids = []
    for item in cart:
        if item['quantity'] > 0:
            item_ids.append(item['id'])

    items_details = Item.query.filter(Item.id.in_(item_ids)).all()

    # Build the shopping cart to display in square
    line_items = []
    for item in cart:
        if item['quantity'] <= 0:
            continue

        details = next((x for x in items_details if x.id == item['id']))
        line_item = {
            "quantity": str(item['quantity']),
            "name": details.name,
            "base_price_money": {
              "amount": int(details.price) * 100,
              "currency": "USD"
            },
            "metadata": {
                "item_id": str(details.id)
            }
          }
        line_items.append(line_item)

    # Build the square order object
    square_order = {
        "idempotency_key": str(uuid.uuid1()),
        "ask_for_shipping_address": False,
        "pre_populate_buyer_email": user.email,
        "redirect_url": f"{CONSTANTS.BASE_URL}{url_for('web_checkout.complete_checkout')}",
        "order": {
            "order": {
                "location_id": CONSTANTS.SQUARE_LOCATION_ID,
                "customer_id": str(user.id),
                "line_items": line_items
            }
        }
    }

    # Make a request to square and redirect to their checkout page on success
    headers = {
        'Square-Version': '2020-11-18',
        'Authorization': f'Bearer {CONSTANTS.SQUARE_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }

    response = requests.post(f'https://{CONSTANTS.SQUARE_API_URL}/v2/locations/{CONSTANTS.SQUARE_LOCATION_ID}/checkouts', data=json.dumps(square_order), headers=headers)

    if response.status_code > 300:
        # Square request failed
        data = response.json()
        errors = data.get('errors', [])
        return {
            "success": False,
            "errors": errors
        }
    else:
        # Successfully made Square request, redirect to checkout page
        data = response.json()
        checkout_url = data['checkout']['checkout_page_url']
        return {
            "success": True,
            "checkout_url": checkout_url
        }


def get_transaction(order: Order):
    # Make a request to square to get transaction info
    headers = {
        'Square-Version': '2020-11-18',
        'Authorization': f'Bearer {CONSTANTS.SQUARE_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }

    transaction_res = requests.get(f'https://{CONSTANTS.SQUARE_API_URL}}/v2/locations/{CONSTANTS.SQUARE_LOCATION_ID}/transactions/{order.square_transaction_id}', headers=headers)

    # Get the order ID from the transaction
    if transaction_res.status_code > 300:
        # Square request failed
        data = transaction_res.json()
        errors = data.get('errors', [])
        return {
            "success": False,
            "errors": errors
        }
    else:
        data = transaction_res.json()
        order_id = data.get('transaction', {}).get('order_id', None)


    # Get order details
    order_res = requests.get(f'https://{CONSTANTS.SQUARE_API_URL}/v2/orders/{order_id}', headers=headers)

    # Get the order details
    if order_res.status_code > 300:
        # Square request failed
        data = order_res.json()
        errors = data.get('errors', [])
        return {
            "success": False,
            "errors": errors
        }
    else:
        data = order_res.json()
        order = data.get('order', {})
        return {
            "success": True,
            "order_details": order
        }
