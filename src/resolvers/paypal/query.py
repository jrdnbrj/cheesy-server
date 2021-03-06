from graphene import ObjectType
from graphene import String, Field, JSONString, List

from ...middleware import authentication_required
from ..type import PayPalOrderType, CartInputType
from ...services.paypal_service import (
    create_order, 
    capture_order, 
    get_order,
    list_orders
)

from decimal import Decimal


class Query(ObjectType):
    create_order = Field(String, amount=String(required=True), discount=String(required=True), 
        shipping=String(required=True), cart=List(CartInputType, required=True), contact_id=String(required=True))
    capture_order = Field(JSONString, order_id=String(required=True), cart=List(CartInputType, required=True),
        contact_id=String(required=True), shipping=String(required=True), discount=String(required=True))
    get_order = Field(JSONString, order_id=String(required=True))
    list_orders = List(PayPalOrderType)

    def resolve_create_order(parent, info, amount, discount, shipping, cart, contact_id):
        print('Creando ando...')
        # order = create_order(round(Decimal(0.02), 2), discount, shipping, cart, contact_id)
        order = create_order(round(Decimal(amount), 2), discount, shipping, cart, contact_id)
        print('Create Order:', order['id'])
        return order['id']
    
    def resolve_capture_order(parent, info, order_id, cart, contact_id, shipping, discount):
        print('Capturando ando...')
        order = capture_order(order_id, cart, contact_id, shipping, discount)
        print('Capture Order:', order)
        return order
    
    @authentication_required()
    def resolve_get_order(parent, info, order_id):
        print('Obteniendo ando...')
        order = get_order(order_id)
        print('Get Order:', order)
        return order

    @authentication_required()
    def resolve_list_orders(parent, info):
        return list_orders()

