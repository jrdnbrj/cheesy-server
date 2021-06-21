from mongoengine.document import Document
from mongoengine.fields import (
    StringField,
    DecimalField,
    DictField,
    DateTimeField
)

from datetime import datetime


class Product(Document):
    name = StringField(required=True, unique=True, max_length=25)
    images = StringField(max_length=1000)
    description = StringField(required=True, max_length=1000)
    short_description = StringField(max_length=500)
    ingredients = StringField(required=True, max_length=500)
    price = DecimalField(precision=2)
    path = StringField(max_length=15)


class PayPalOrder(Document):
    order_id = StringField()
    status = StringField()
    value = DecimalField(precision=2)
    name = StringField()
    surname = StringField()
    full_name = StringField()
    payer_id = StringField()
    email = StringField()
    address = DictField()
    capture_id  = StringField()
    capture_status = StringField()
    purchase_breakdown = DictField()
    capture_time = DateTimeField(default=datetime.utcnow)
    create_time = DateTimeField()
    update_time = DateTimeField()

