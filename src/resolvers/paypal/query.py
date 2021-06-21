from graphene import ObjectType
from graphene import String, Field, JSONString

from ...services.paypal_service import create_order, capture_order


class Query(ObjectType):
    create_order = Field(String)
    capture_order = Field(JSONString, order_id=String(required=True))

    def resolve_create_order(parent, info):
        order = create_order()
        print('Create Order:', order['id'])
        return order['id']
    
    def resolve_capture_order(parent, info, order_id):
        print('Capturando ando...')
        order = capture_order(order_id)
        print('Capture Order:', order)
        return order

