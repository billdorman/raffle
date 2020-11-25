from extensions import db, ma
from datetime import datetime
from marshmallow import fields, post_load, validate
from flask_login import UserMixin
import config.const as CONST
import logging

log = logging.getLogger()


# This class represents a user record in the database
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(50))
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(30))
    address = db.Column(db.String(35))
    city = db.Column(db.String(30))
    state = db.Column(db.String(25))
    zip = db.Column(db.String(10))
    phone = db.Column(db.String(25))
    email = db.Column(db.String(50))
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean, default=True)
    comments = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def update(self, user_data=None):
        log.info("Preparing to update user")
        if user_data is None:
            user_data = {}

        self.role = user_data.get("role", self.role)
        self.first_name = user_data.get("first_name", self.first_name)
        self.last_name = user_data.get("last_name", self.last_name)
        self.address = user_data.get("address", self.address)
        self.city = user_data.get("city", self.city)
        self.state = user_data.get("state", self.state)
        self.zip = user_data.get("zip", self.zip)
        self.phone = user_data.get("phone", self.phone)
        self.email = user_data.get("email", self.email)
        self.password = user_data.get("password", self.password)
        self.active = user_data.get("active", self.active)
        self.comments = user_data.get("comments", self.comments)
        self.created_at = user_data.get("created_at", self.created_at)
        self.updated_at = user_data.get("updated_at", self.updated_at)
        db.session.add(self)
        db.session.commit()
        return self


class UserSchema(ma.Schema):
    class Meta:
        # load_only specifies a list of fields that will only be loaded and never serialized for outputting to a user
        load_only = ['password']

    id = fields.Integer()

    role = fields.String(allow_none=True, validate=validate.OneOf(['administrator', 'user']))

    first_name = fields.String(allow_none=True, validate=validate.Length(max=20))

    last_name = fields.String(allow_none=True, validate=validate.Length(max=30))

    address = fields.String(allow_none=True, validate=validate.Length(max=35))

    city = fields.String(allow_none=True, validate=validate.Length(max=30))

    state = fields.String(allow_none=True, validate=validate.OneOf(CONST.STATE_ABBREVIATIONS))

    zip = fields.String(allow_none=True, validate=validate.Length(max=10))

    phone = fields.String(allow_none=True, validate=validate.Regexp("^\d{10}$"))

    email = fields.String()

    password = fields.String(allow_none=True)

    active = fields.Boolean(default=True)

    comments = fields.String(allow_none=True)

    created_at = fields.String(allow_none=True)

    updated_at = fields.String(allow_none=True)


    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)
