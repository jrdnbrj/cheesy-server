from graphene import ObjectType, InputObjectType
from graphene import (
    String, 
    Decimal, 
    List, 
    Int, 
    DateTime, 
    JSONString, 
    Boolean
)


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


class CartType(InputObjectType):
    path = String()
    amount = Int(required=True)
    price = Decimal(required=True)
    image = String()
    name = String()
    total = Decimal(required=True)
    bundle_up = Int()
    buy_once = Boolean()
    join_club = Boolean()
    interval = Int()
    choose1 = String()
    choose3 = List(List(String))


class ContactType(ObjectType):
    id = String()
    full_name = String()
    email = String()
    phone = String()
    message = String()


class HomeType(ObjectType):
    name = String()
    description = String()
    sequence = Int()


class HomeInputType(InputObjectType):
    name = String()
    description = String()


class OurFamilyType(ObjectType):
    title = String()
    description = String()
    sequence = Int()


class OurFamilyInputType(InputObjectType):
    title = String()
    description = String()


class CouponType(ObjectType):
    code = String()
    discount = String()
    is_active = Boolean()


class SettingsType(ObjectType):
    discount_month = String()
    discount_2months = String()


class InstagramMediaType(ObjectType):
    url = String()
    image = String()


class CheckoutInfoInputType(InputObjectType):
    name = String(required=True)
    phone = String(required=True)
    email = String(required=True)
    address = String(required=True)
    address2 = String(required=True)
    city = String(required=True)
    state = String(required=True)
    zip_code = String(required=True)


class CheckoutInfoType(ObjectType):
    name = String(required=True)
    phone = String(required=True)
    email = String(required=True)
    address = String(required=True)
    address2 = String(required=True)
    city = String(required=True)
    state = String(required=True)
    zip_code = String(required=True)


class CheckoutContactType(ObjectType):
    shipping_information = CheckoutInfoType()
    billing_information = CheckoutInfoType()


class ShippingStateType(ObjectType):
    state = String()
    value = Decimal()


class ShippingStateInputType(ObjectType):
    state = String()
    value = Decimal()


class ShippingResponseType(ObjectType):
    response = Boolean()
    value = String()


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
