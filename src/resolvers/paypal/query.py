from graphene import ObjectType
from graphene import String, Field, JSONString, List

from ...services.paypal_service import (
    create_order, 
    capture_order, 
    list_orders,
    create_product, 
    list_products, 
    list_plans, 
    create_plan,
    create_subscription,
    show_subscription_details,
    activate_subscription
)

from ..type import PayPalOrderType


class Query(ObjectType):
    create_order = Field(String)
    capture_order = Field(JSONString, order_id=String(required=True))
    list_orders = List(PayPalOrderType)
    list_products = Field(JSONString)
    create_product = Field(JSONString)
    list_plans = Field(JSONString)
    create_plan = Field(JSONString)
    create_subscription = Field(JSONString)
    show_subscription_details = Field(JSONString)
    activate_subscription = Field(JSONString)

    def resolve_create_order(parent, info):
        print('Creando ando...')
        order = create_order()
        print('Create Order:', order['id'])
        return order['id']
    
    def resolve_capture_order(parent, info, order_id):
        print('Capturando ando...')
        order = capture_order(order_id)
        print('Capture Order:', order)
        return order
    
    def resolve_list_orders(parent, info):
        return list_orders()

    def resolve_list_products(parent, info):
        return list_products()

    def resolve_create_product(parent, info):
        return create_product()
    
    def resolve_list_plans(parent, info):
        return list_plans()

    def resolve_create_plan(parent, info):
        return create_plan()
    
    def resolve_create_subscription(parent, info):
        return create_subscription()

    def resolve_show_subscription_details(parent, info):
        return show_subscription_details()

    def resolve_activate_subscription(parent, info):
        return activate_subscription()

