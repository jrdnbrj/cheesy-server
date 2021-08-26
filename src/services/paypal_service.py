from ..db.documents import PayPal, Order, PayPalPaymentError

from .checkout_service import get_checkout_contact

from .utils import to_cart_object, to_paypal_object, validate_amount

from paypalcheckoutsdk.core import (
    PayPalHttpClient, 
    SandboxEnvironment, 
    LiveEnvironment
)
from paypalcheckoutsdk.orders import (
    OrdersCreateRequest, 
    OrdersCaptureRequest,
    OrdersGetRequest
)

from decouple import config


class _PayPalClient:

    def __init__(self):
        self.client_id_sandbox = config('PAYPAL_CLIENT_ID_SANDBOX')
        self.client_secret_sandbox = config('PAYPAL_CLIENT_SECRET_SANDBOX')

        self.client_id = config('PAYPAL_CLIENT_ID')
        self.client_secret = config('PAYPAL_CLIENT_SECRET')

        print('PayPalClient:', config('PAYPAL_ENVIRONMENT'), self.client_id, self.client_secret)

        if config('PAYPAL_ENVIRONMENT') == 'sandbox':
            self.environment = SandboxEnvironment(client_id=self.client_id_sandbox, client_secret=self.client_secret_sandbox)
        elif config('PAYPAL_ENVIRONMENT') == 'live':
            self.environment = LiveEnvironment(client_id=self.client_id, client_secret=self.client_secret)

        self.client = PayPalHttpClient(self.environment)


class _CreateOrder(_PayPalClient):

    def create_order(self, request_body):
        request = OrdersCreateRequest()
        request.prefer('return=representation')
        request.request_body(request_body)
        return self.client.execute(request)


class _CaptureOrder(_PayPalClient):

    def capture_order(self, order_id):
        request = OrdersCaptureRequest(order_id)
        return self.client.execute(request)


class _GetOrder(_PayPalClient):

    def get_order(self, order_id):
        request = OrdersGetRequest(order_id)
        return self.client.execute(request)


def create_order(amount, discount, shipping, cart, contact_id):
    print('amount:', amount)

    # if not validate_amount(cart, shipping, discount, amount):
    #     PayPalPaymentError(
    #         contact_id=contact_id,
    #         amount=amount,
    #         detail="Amount does not match with Cart's items."
    #     ).save()
    #     raise Exception("Amount does not match with Cart's items.")

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
                        #     "value": discount
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
    return order.result.__dict__['_dict']


def capture_order(order_id, cart, contact_id, shipping, discount):
    order = _CaptureOrder().capture_order(order_id)
    order = order.result.__dict__['_dict']
    print('Order:', order)

    contact = get_checkout_contact(contact_id)

    try:
        Order(
            cart=to_cart_object(cart), 
            paypal=to_paypal_object(order), 
            checkout_info=contact.to_json(),
            shipping=shipping,
            discount=discount
        ).save()
    except Exception as e:
        print('New Order Error:', e)
        PayPalPaymentError(
            order_id=order_id,
            contact_id=contact_id,
            detail='In Caputre Order: {}'.format(e)
        ).save()
    return order


def get_order(order_id):
    order = _GetOrder().get_order(order_id)
    return order.result.__dict__['_dict']


def list_orders():
    return PayPal.objects()

