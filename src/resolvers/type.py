from graphene import ObjectType
from graphene import String, Int, Boolean, Date, Decimal


class ProductType(ObjectType):
    id = String(required=True)
    name = String()
    description = String()
    short_description = String()
    ingredients = String()
    price = Decimal()
