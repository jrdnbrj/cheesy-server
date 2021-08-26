from graphene import ObjectType
from graphene import String, Field, JSONString, List

from ..type import CartInputType, SquarePaymentErrorType
from ...middleware import authentication_required
from ...services.square_service import (
    list_payments,
    get_payment,
    create_payment, 
    retrieve_subscription,
    cancel_subscription,
    list_invoices,
    list_square_errors
)

from decimal import Decimal


class Query(ObjectType):
    list_payments = Field(JSONString)
    get_payment = Field(JSONString, payment_id=String(required=True))
    create_payment = Field(String, payment_token=String(required=True), amount=String(required=True), contact_id=String(required=True),
        cart=List(CartInputType, required=True), shipping=String(required=True), discount=String(required=True))
    retrieve_subscription = Field(JSONString, subscription_id=String(required=True))
    cancel_subscription = Field(String, subscription_id=String(required=True))
    list_invoices = Field(JSONString)
    list_square_errors = List(SquarePaymentErrorType)

    @authentication_required()
    def resolve_list_payments(parent, info):
        return list_payments()

    @authentication_required()
    def resolve_get_payment(parent, info, payment_id):
        return get_payment(payment_id)

    def resolve_create_payment(parent, info, payment_token, amount, contact_id, cart, shipping, discount):
        # amount = Decimal(0.02)
        amount = Decimal(amount)
        return create_payment(payment_token, round(amount, 2), contact_id, cart, shipping, discount)

    @authentication_required()
    def resolve_retrieve_subscription(parent, info, subscription_id):
        return retrieve_subscription(subscription_id)

    @authentication_required()
    def resolve_cancel_subscription(parent, info, subscription_id):
        return cancel_subscription(subscription_id)

    @authentication_required()
    def resolve_list_invoices(parent, info):
        return list_invoices()

    @authentication_required()
    def resolve_list_square_errors(parent, info):
        return list_square_errors()
    