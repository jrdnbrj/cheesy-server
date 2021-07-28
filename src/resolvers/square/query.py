from graphene import ObjectType
from graphene import String, Field, JSONString, List

from ..type import CartType
from ...middleware import authentication_required
from ...services.square_service import (
    list_payments,
    create_payment, 
    list_customers,
    # create_customer,
    list_cards,
    # create_card,
    get_catalog_info,
    # upsert_catalog, 
    list_catalogs,
    create_subscription,
    list_invoices
)

from decimal import Decimal


class Query(ObjectType):
    list_payments = Field(JSONString)
    create_payment = Field(String, payment_token=String(required=True), amount=String(required=True), contact_id=String(required=True),
        cart=List(CartType, required=True), shipping=String(required=True), discount=String(required=True))
    list_customers = Field(JSONString)
    # create_customer = Field(String)
    list_cards = Field(String)
    # create_card = Field(String)
    get_catalog_info = Field(String)
    list_catalogs = Field(JSONString)
    # upsert_catalog = Field(String)
    create_square_subscription = Field(String)
    list_invoices = Field(JSONString)

    @authentication_required()
    def resolve_list_payments(parent, info):
        return list_payments()

    def resolve_create_payment(parent, info, payment_token, amount, contact_id, cart, shipping, discount):
        amount = Decimal(amount)
        return create_payment(payment_token, round(amount, 2), contact_id, cart, shipping, discount)

    @authentication_required()
    def resolve_list_customers(parent, info):
        return list_customers()

    # @authentication_required()
    # def resolve_create_customer(parent, info):
    #     create_customer()
    #     return 'OK'

    @authentication_required()
    def resolve_list_cards(parent, info):
        list_cards()
        return 'OK'
    
    # @authentication_required()
    # def resolve_create_card(parent, info):
    #     create_card()
    #     return 'OK'

    @authentication_required()
    def resolve_get_catalog_info(parent, info):
        get_catalog_info()
        return 'OK'

    @authentication_required()
    def resolve_list_catalogs(parent, info):
        return list_catalogs()

    # @authentication_required()
    # def resolve_upsert_catalog(parent, info):
    #     upsert_catalog()
    #     return 'OK'

    @authentication_required()
    def resolve_create_square_subscription(parent, info):
        create_subscription()
        return 'OK'

    @authentication_required()
    def resolve_list_invoices(parent, info):
        return list_invoices()
    