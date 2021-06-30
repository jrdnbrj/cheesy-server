from graphene import ObjectType
from graphene import String, Decimal, List


class ProductType(ObjectType):
    id = String(required=True)
    name = String()
    images = List(String)
    smoothies = List(String)
    description = String()
    short_description = String()
    ingredients = List(String)
    price = Decimal()
    path = String()


class ContactType(ObjectType):
    full_name = String()
    email = String()
    phone = String()
    message = String()