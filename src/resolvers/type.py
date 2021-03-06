from graphene import ObjectType, InputObjectType
from graphene import (
    String, 
    Decimal, 
    List, 
    Int, 
    DateTime, 
    JSONString, 
    Boolean,
    Field
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
    percentage = Decimal()
    path = String()
    sequence = Int()


class CartInputType(InputObjectType):
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


class CartType(ObjectType):
    amount = Int(required=True)
    price = Decimal(required=True)
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
    discount_month = Decimal()
    discount_2months = Decimal()


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


class CheckoutContactTypeF(ObjectType):
    shipping_information = Field(CheckoutInfoType)
    billing_information = Field(CheckoutInfoType)


class ShippingStateType(ObjectType):
    state = String()
    value = Decimal()


class ShippingResponseType(ObjectType):
    response = Boolean()
    value = String()


class SquareType(ObjectType):
    created_at = DateTime()
    status = String()
    buyer_email_address = String()
    total_money = Decimal()

    # PAYMENT FIELDS
    payment_id = String()
    
    # SUBSCRIPTION FIELDS
    subscription_id = String()
    start_date = DateTime()


class SquarePaymentErrorType(ObjectType):
    category = String()
    code = String()
    detail = String()
    field = String()
    customer_id = String()
    card_id = String()
    amount = Decimal()
    type = String()
    created_at = DateTime()


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


class OrderType(ObjectType):
    type = String()
    cart = List(CartType)
    square = Field(SquareType)
    paypal = Field(PayPalOrderType)
    checkout_info = Field(CheckoutContactTypeF)
    shipping = Decimal()
    discount = Decimal()
    created_at = DateTime()
