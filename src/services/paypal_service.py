from ..db.documents import PayPalOrder

from paypalcheckoutsdk.core import (
    PayPalHttpClient, 
    SandboxEnvironment, 
    LiveEnvironment
)
from paypalcheckoutsdk.orders import (
    OrdersCreateRequest, 
    OrdersGetRequest, 
    OrdersCaptureRequest
)

from decouple import config

from decimal import Decimal
from datetime import datetime


class _PayPalClient:

    def __init__(self):
        self.client_id = config('PAYPAL_CLIENT_ID')
        self.client_secret = config('PAYPAL_CLIENT_SECRET')
        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        # self.environment = LiveEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        self.client = PayPalHttpClient(self.environment)


class _CreateOrder(_PayPalClient):

    def create_order(self, request_body):
        request = OrdersCreateRequest()
        request.prefer('return=representation')
        request.request_body(request_body)
        response = self.client.execute(request)

        return response


class _GetOrder(_PayPalClient):
  
    def get_order(self, order_id):
        request = OrdersGetRequest(order_id)
        response = self.client.execute(request)
        return response


class _CaptureOrder(_PayPalClient):

    def capture_order(self, order_id):
        request = OrdersCaptureRequest(order_id)
        response = self.client.execute(request)
        return response


def create_order():
    request_body = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {
                    "currency_code": "USD",
                    "value": 24.55,
                    "breakdown": {
                        "item_total": {
                            "currency_code": "USD",
                            "value": 24.55
                        },
                    }
                }
            }
        ]
    }

    order = _CreateOrder().create_order(request_body)
    data = order.result.__dict__['_dict']

    return data


def capture_order(order_id):
    order = _CaptureOrder().capture_order(order_id)
    order = order.result.__dict__['_dict']
    # print('DATAAA:', order)

    try:
        new_order = PayPalOrder(
            order_id = order['id'],
            status = order['status'],
            value = Decimal(order['purchase_units'][0]['payments']['captures'][0]['amount']['value']),
            name = order['payer']['name']['given_name'],
            surname = order['payer']['name']['surname'],
            full_name = order['purchase_units'][0]['shipping']['name']['full_name'],
            payer_id = order['payer']['payer_id'],
            email = order['payer']['email_address'],
            address = order['purchase_units'][0]['shipping']['address'],
            capture_id = order['purchase_units'][0]['payments']['captures'][0]['id'],
            capture_status = order['purchase_units'][0]['payments']['captures'][0]['status'],
            purchase_breakdown = order['purchase_units'][0]['payments']['captures'][0]['seller_receivable_breakdown'],
            create_time = datetime.strptime(order['purchase_units'][0]['payments']['captures'][0]['create_time'], "%Y-%m-%dT%H:%M:%SZ"),
            update_time = datetime.strptime(order['purchase_units'][0]['payments']['captures'][0]['update_time'], "%Y-%m-%dT%H:%M:%SZ"),
        )
        new_order.save()
    except Exception:
        print('New Order Error:', Exception)

    return order