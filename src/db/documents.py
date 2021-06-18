from mongoengine.document import Document
from mongoengine.fields import (
    StringField,
    DecimalField
)


class Product(Document):
    name = StringField(required=True, unique=True, max_length=25)
    images = StringField(max_length=1000)
    description = StringField(required=True, max_length=1000)
    short_description = StringField(max_length=500)
    ingredients = StringField(required=True, max_length=500)
    price = DecimalField(precision=2)
    path = StringField(max_length=15)
