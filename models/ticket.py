from extensions import db, ma
from datetime import datetime
from marshmallow import fields, post_load
from models.item_image import ItemImageSchema
from models.item import Item, ItemSchema
import logging

log = logging.getLogger()


# This class represents an item record in the database
class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    active = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    item = db.relationship('Item')


    def update(self, ticket_data=None):
        log.info("Preparing to update ticket")
        if ticket_data is None:
            ticket_data = {}

        self.user_id = ticket_data.get("user_id", self.user_id)
        self.item_id = ticket_data.get("item_id", self.item_id)
        self.order_id = ticket_data.get("order_id", self.order_id)
        self.active = ticket_data.get("active", self.active)
        self.created_at = ticket_data.get("created_at", self.created_at)
        self.updated_at = ticket_data.get("updated_at", self.updated_at)
        db.session.add(self)
        db.session.commit()
        return self


class TicketSchema(ma.Schema):

    id = fields.Integer()

    user_id = fields.Integer()

    item_id = fields.Integer()

    order_id = fields.Integer()

    active = fields.Boolean()

    created_at = fields.String(allow_none=True)

    updated_at = fields.String(allow_none=True)

    images = fields.Nested(ItemImageSchema, many=True)

    item = fields.Nested(ItemSchema)

    @post_load
    def make_ticket(self, data, **kwargs):
        return Ticket(**data)
