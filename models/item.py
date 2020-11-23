from extensions import db, ma
from datetime import datetime
from marshmallow import fields, post_load, validate
from models.item_image import ItemImageSchema
import logging

log = logging.getLogger()


# This class represents an item record in the database
class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    description = db.Column(db.String(250))
    price = db.Column(db.Float)
    available = db.Column(db.Boolean)
    category = db.Column(db.String(255))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    images = db.relationship('ItemImage', backref='item')

    def update(self, item_data=None):
        log.info("Preparing to update item")
        if item_data is None:
            item_data = {}

        self.name = item_data.get("name", self.name)
        self.description = item_data.get("description", self.description)
        self.price = item_data.get("price", self.price)
        self.available = item_data.get("available", self.available)
        self.category = item_data.get("category", self.category)
        self.created_by = item_data.get("created_by", self.created_by)
        self.created_at = item_data.get("created_at", self.created_at)
        self.updated_at = item_data.get("updated_at", self.updated_at)
        db.session.add(self)
        db.session.commit()
        return self


class ItemSchema(ma.Schema):

    id = fields.Integer()

    name = fields.String()

    description = fields.String(allow_none=True, validate=validate.Length(max=250))

    price = fields.Float(allow_none=True)

    available = fields.Boolean()

    category = fields.String()

    created_by = fields.Integer()

    created_at = fields.String(allow_none=True)

    updated_at = fields.String(allow_none=True)

    images = fields.Nested(ItemImageSchema, many=True)

    @post_load
    def make_item(self, data, **kwargs):
        return Item(**data)
