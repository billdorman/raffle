from extensions import db, ma
from datetime import datetime
from marshmallow import fields, post_load
from models.ticket import TicketSchema
import logging

log = logging.getLogger()


# This class represents an item record in the database
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    square_checkout_id = db.Column(db.String(50))
    square_order_id = db.Column(db.String(50))
    square_reference_id = db.Column(db.String(50))
    square_transaction_id = db.Column(db.String(50))
    payment_status = db.Column(db.String(50))
    order_total = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    tickets = db.relationship('Ticket', backref='order')

    def update(self, order_data=None):
        log.info("Preparing to update order")
        if order_data is None:
            order_data = {}

        self.user_id = order_data.get("user_id", self.user_id)
        self.square_checkout_id = order_data.get("square_checkout_id", self.square_checkout_id)
        self.square_order_id = order_data.get("square_order_id", self.square_order_id)
        self.square_reference_id = order_data.get("square_reference_id", self.square_reference_id)
        self.square_transaction_id = order_data.get("square_transaction_id", self.square_transaction_id)
        self.payment_status = order_data.get("payment_status", self.payment_status)
        self.order_total = order_data.get("order_total", self.order_total)
        self.created_at = order_data.get("created_at", self.created_at)
        self.updated_at = order_data.get("updated_at", self.updated_at)
        db.session.add(self)
        db.session.commit()
        return self


class OrderSchema(ma.Schema):

    id = fields.Integer()

    user_id = fields.Integer()

    square_checkout_id = fields.String()

    square_order_id = fields.String()

    square_reference_id = fields.String()

    square_transaction_id = fields.String()

    payment_status = fields.String()

    order_total = fields.Float()

    created_at = fields.String(allow_none=True)

    updated_at = fields.String(allow_none=True)

    tickets = fields.Nested(TicketSchema, many=True)

    @post_load
    def make_order(self, data, **kwargs):
        return Order(**data)
