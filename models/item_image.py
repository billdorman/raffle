from extensions import db, ma
from datetime import datetime
from marshmallow import fields, post_load, validate
from flask_login import UserMixin
import logging

log = logging.getLogger()


# This class represents an item record in the database
class ItemImage(db.Model):
    __tablename__ = 'item_images'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    path = db.Column(db.String(255))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def update(self, image_data=None):
        log.info("Preparing to update item image")
        if image_data is None:
            image_data = {}

        self.path = image_data.get("path", self.path)
        self.created_by = image_data.get("created_by", self.created_by)
        self.created_at = image_data.get("created_at", self.created_at)
        self.updated_at = image_data.get("updated_at", self.updated_at)
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        log.info("Preparing to delete item image")
        db.session.delete(self)
        db.session.commit()


class ItemImageSchema(ma.Schema):

    id = fields.Integer()

    item_id = fields.Integer()

    path = fields.String(validate=validate.Length(max=255))

    created_by = fields.Integer()

    created_at = fields.String(allow_none=True)

    updated_at = fields.String(allow_none=True)

    @post_load
    def make_item_image(self, data, **kwargs):
        return ItemImage(**data)
