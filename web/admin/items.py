from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from flask_login import login_required, current_user
from models.item import Item
from models.item_image import ItemImage, ItemImageSchema
from config import const as CONSTANTS
import logging
import uuid
import os

log = logging.getLogger()
web_admin_items = Blueprint('web_admin_items', __name__)


# context_processor used for loading global blueprint variables
@web_admin_items.context_processor
def inject_globals():
    return dict(user=current_user)


# Route used to display the items page
@web_admin_items.route("", methods=['GET'])
@login_required
def items_get():
    log.info("web_admin_items.items_get")

    items = Item.query.all()

    return render_template('admin/items.html', items=items)


# Route used to display the item edit page
@web_admin_items.route("<id>/edit", methods=['GET'])
@login_required
def item_edit(id):
    log.info("web_admin_items.item_edit")

    item = Item.query.get(id)

    return render_template('admin/item-edit.html', item=item, categories=CONSTANTS.ITEM_CATEGORIES)


# Route used to display the new item page
@web_admin_items.route("/new", methods=['GET'])
@login_required
def item_new():
    log.info("web_admin_items.item_new")

    item = Item()
    item.name = "New Item"
    item.description = ""
    item.price = 1
    item.created_by = current_user.id
    item.update()

    return redirect(url_for('web_admin_items.item_edit', id=item.id))

# Route used to edit a user
@web_admin_items.route("/<id>/edit", methods=['POST'])
@login_required
def edit_page(id):
    log.info("web_admin_items.edit_page")
    # Get a reference to the item to edit
    item = Item.query.get(id)

    # POST
    item.update({
        "name": request.form['name'],
        "description": request.form['description'],
        "price": float(request.form['price']),
        "available": True if request.form['available'] == "True" else False,
        "category": request.form['category']
    })

    # Return the item list page
    items = Item.query.all()
    return render_template('admin/items.html', items=items)


# Route used to delete the specified item
@web_admin_items.route("<id>/delete", methods=['GET'])
@login_required
def item_delete(id):
    log.info("web_admin_items.item_delete")
    item = Item.query.get(id)

    # Remove the database record
    item.delete()

    # Load the item list page
    return redirect(url_for('web_admin_items.items_get'))


# Route used to upload an item image
@web_admin_items.route("<id>/image", methods=['POST'])
@login_required
def item_image_upload(id):
    log.info("web_admin_items.item_image_upload")
    item_image_schema = ItemImageSchema()

    # Get a reference to the uploaded file(s)
    file = request.files['filepond']
    print(file.filename)
    print(file.content_type)

    # Build a unique filename to save the file
    extension = file.filename.split(".")[1]
    unique_id = str(uuid.uuid4())
    filename = f'{ unique_id }.{ extension }'

    # Save the file to /static/images/items/{item_id}
    file.save(os.path.join("static", "images", "items", filename))

    # Create a database record
    image = ItemImage()
    image.item_id = id
    image.path = f"static/images/items/{filename}"
    image.created_by = current_user.id
    image.update()

    # Build a dictionary from the JobImage object for returning to the client
    image = item_image_schema.dump(image)

    # Build our response
    response = {
        'image': image
    }
    return jsonify(response)


# Route used to delete the specified image
@web_admin_items.route("<id>/image/<image_id>", methods=['GET'])
@login_required
def item_image_delete(id, image_id):
    log.info("web_admin_items.item_image_delete")
    item = Item.query.get(id)
    image = ItemImage.query.get(image_id)

    print(os.path.basename(image.path))

    # Delete the file on disk
    if os.path.exists(image.path):
        os.remove(image.path)  # one file at a time

    # Remove the database record
    image.delete()

    # Load the item edit page
    return render_template('admin/item-edit.html', item=item, categories=CONSTANTS.ITEM_CATEGORIES)
