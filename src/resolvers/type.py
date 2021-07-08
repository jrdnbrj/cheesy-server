from graphene import ObjectType
from graphene import String, Decimal, List, Int

class SmoothieType(ObjectType):
    name = String()
    path = String()
    ingredients = String()


class ProductType(ObjectType):
    id = String(required=True)
    name = String()
    images = List(String)
    smoothies = List(List(String))
    description = String()
    short_description = String()
    ingredients = List(String)
    price = Decimal()
    path = String()
    sequence = Int()


class ContactType(ObjectType):
    id = String()
    full_name = String()
    email = String()
    phone = String()
    message = String()
