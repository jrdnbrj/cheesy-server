from graphene import ObjectType
from graphene import String, Decimal, List, Int, DateTime, JSONString

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


class PayPalOrderType(ObjectType):
    order_id = String()
    status = String()
    value = Decimal()
    name = String()
    surname = String()
    full_name = String()
    payer_id = String()
    email = String()
    address = JSONString()
    capture_id  = String()
    capture_status = String()
    purchase_breakdown = JSONString()
    capture_time = DateTime()
    create_time = DateTime()
    update_time = DateTime()
