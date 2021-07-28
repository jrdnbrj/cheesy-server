from graphene import ObjectType
from graphene import String, Field, JSONString, List

from ..type import CartInputType, SquarePaymentErrorType
from ...middleware import authentication_required
from ...services.square_service import (
    list_payments,
    create_payment, 
    list_customers,
    list_cards,
    list_catalogs,
    list_invoices,
    list_square_errors
)

from decimal import Decimal


class Query(ObjectType):
    list_payments = Field(JSONString)
    create_payment = Field(String, payment_token=String(required=True), amount=String(required=True), contact_id=String(required=True),
        cart=List(CartInputType, required=True), shipping=String(required=True), discount=String(required=True))
    list_customers = Field(JSONString)
    list_cards = Field(String)
    list_catalogs = Field(JSONString)
    list_invoices = Field(JSONString)
    list_square_errors = List(SquarePaymentErrorType)

    @authentication_required()
    def resolve_list_payments(parent, info):
        return list_payments()

    def resolve_create_payment(parent, info, payment_token, amount, contact_id, cart, shipping, discount):
        amount = Decimal(amount)
        return create_payment(payment_token, round(amount, 2), contact_id, cart, shipping, discount)

    @authentication_required()
    def resolve_list_customers(parent, info):
        return list_customers()

    @authentication_required()
    def resolve_list_cards(parent, info):
        list_cards()
        return 'OK'

    @authentication_required()
    def resolve_list_catalogs(parent, info):
        return list_catalogs()

    @authentication_required()
    def resolve_list_invoices(parent, info):
        return list_invoices()

    @authentication_required()
    def resolve_list_square_errors(parent, info):
        return list_square_errors()
    