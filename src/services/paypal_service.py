from ..db.documents import PayPal, Order

from .checkout_service import get_checkout_contact

from paypalcheckoutsdk.core import (
    PayPalHttpClient, 
    SandboxEnvironment, 
    LiveEnvironment
)
from paypalcheckoutsdk.orders import (
    OrdersCreateRequest, 
    OrdersCaptureRequest
)

from decouple import config

from decimal import Decimal
from datetime import datetime


authorization = 'Bearer '

class _PayPalClient:

    def __init__(self):
        self.client_id = config('PAYPAL_CLIENT_ID')
        self.client_secret = config('PAYPAL_CLIENT_SECRET')

        # print('PayPalClient:', type(config('PAYPAL_ENVIRONMENT')), config('PAYPAL_ENVIRONMENT'), config('PAYPAL_ENVIRONMENT') == 'sandbox', config('PAYPAL_ENVIRONMENT') == 'live')

        if config('PAYPAL_ENVIRONMENT') == 'sandbox':
            self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        elif config('PAYPAL_ENVIRONMENT') == 'live':
            self.environment = LiveEnvironment(client_id=self.client_id, client_secret=self.client_secret)

        self.client = PayPalHttpClient(self.environment)


class _CreateOrder(_PayPalClient):

    def create_order(self, request_body):
        request = OrdersCreateRequest()
        request.prefer('return=representation')
        request.request_body(request_body)
        response = self.client.execute(request)

        return response


class _CaptureOrder(_PayPalClient):

    def capture_order(self, order_id):
        request = OrdersCaptureRequest(order_id)
        response = self.client.execute(request)
        return response


def create_order(amount):
    print('amount:', amount)
    request_body = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {
                    "currency_code": "USD",
                    "value": str(amount),
                    "breakdown": {
                        "item_total": {
                            "currency_code": "USD",
                            "value": str(amount)
                        },
                        # "discount": {
                        #     "currency_code": "USD",
                        #     "value": "10.24"
                        # },
                    }
                },
                
                # "items": [
                #     {
                #         "name": "item1",
                #         "unit_amount": {
                #             "currency_code": "USD",
                #             "value": "29.05"
                #         }, 
                #         "quantity": 1,
                #     },
                #     {
                #         "name": "item2",
                #         "unit_amount": {
                #             "currency_code": "USD",
                #             "value": "10"
                #         }, 
                #         "quantity": 2,
                #     }
                # ]
            }
        ]
    }

    order = _CreateOrder().create_order(request_body)
    data = order.result.__dict__['_dict']

    return data


def capture_order(order_id, cart, contact_id, shipping, discount):
    order = _CaptureOrder().capture_order(order_id)
    order = order.result.__dict__['_dict']
    print('Cart:', cart)

    contact = get_checkout_contact(contact_id)

    try:
        Order(
            cart=to_cart_object(cart), 
            paypal=to_paypal_object(order), 
            checkout_info=contact.to_json()
        ).save()
    except Exception as e:
        print('New Order Error:', e)

    return order


def list_orders():
    return PayPal.objects()


# UTILS


def to_cart_object(cart):
    new_cart = []
    for item in cart:
        new_item = {
            "amount": item.amount,
            "price": item.price,
            "name": item.name,
            "total": item.total,
            "bundle_up": item.bundle_up,
            "buy_once": item.buy_once,
            "join_club": item.join_club,
            "interval": item.interval,
            "choose1": item.choose1,
            "choose3": item.choose3
        }
        new_cart.append(new_item)
    
    return new_cart

def to_paypal_object(order):
    return {
        "order_id": order['id'],
        "status": order['status'],
        "value": Decimal(order['purchase_units'][0]['payments']['captures'][0]['amount']['value']),
        "name": order['payer']['name']['given_name'],
        "surname": order['payer']['name']['surname'],
        "full_name": order['purchase_units'][0]['shipping']['name']['full_name'],
        "payer_id": order['payer']['payer_id'],
        "email": order['payer']['email_address'],
        "address": order['purchase_units'][0]['shipping']['address'],
        "capture_id": order['purchase_units'][0]['payments']['captures'][0]['id'],
        "capture_status": order['purchase_units'][0]['payments']['captures'][0]['status'],
        "purchase_breakdown": order['purchase_units'][0]['payments']['captures'][0]['seller_receivable_breakdown'],
        "create_time": datetime.strptime(order['purchase_units'][0]['payments']['captures'][0]['create_time'], "%Y-%m-%dT%H:%M:%SZ"),
        "update_time": datetime.strptime(order['purchase_units'][0]['payments']['captures'][0]['update_time'], "%Y-%m-%dT%H:%M:%SZ"),
    }
