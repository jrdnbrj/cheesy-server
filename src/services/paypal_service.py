from ..db.documents import PayPalOrder

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
import requests
import uuid
import json


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
                    }
                }
            }
        ]
    }

    order = _CreateOrder().create_order(request_body)
    data = order.result.__dict__['_dict']

    return data


def capture_order(order_id, cart):
    order = _CaptureOrder().capture_order(order_id)
    order = order.result.__dict__['_dict']
    print('Cart:', cart)

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


def list_orders():
    return PayPalOrder.objects()


def list_products():
    url = 'https://api-m.sandbox.paypal.com/v1/catalogs/products?total_required=true'
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer ",
    }
    response = requests.get(url, headers=headers)
    print('List Products:', response.json())
    return response.json()


def create_product():
    url = 'https://api-m.sandbox.paypal.com/v1/catalogs/products'
    headers = {
        "Content-Type": "application/json",
        "Authorization": authorization,
        "PayPal-Request-Id": str(uuid.uuid4())
    }
    data = {
        "name": "Cheesy Bittes Club",
        "description": "Multiple Products of Cheesy Bittes",
        "type": "SERVICE",
        "category": "FOOD_PRODUCTS",
        "image_url": "https://144.126.222.169/static/products-mix.png",
        "home_url": "https://cheesybittes.netlify.app/products"
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print('Create Product:', response.json())
    return response.json()


def list_plans():
    url = 'https://api-m.sandbox.paypal.com/v1/billing/plans?total_required=true'
    headers = {
        "Content-Type": "application/json",
        "Authorization": authorization,
    }
    response = requests.get(url, headers=headers)
    print('List Plans:', response.json())
    return response.json()


def create_plan():
    url = 'https://api-m.sandbox.paypal.com/v1/billing/plans'
    headers = {
        "Content-Type": "application/json",
        "Authorization": authorization,
    }
    data = {
        "name": "Cheesy Bittes Plan",
        "description": "Cheesy Bittes CLub",
        "product_id": "PROD-0YL16247R9828743U",
        "billing_cycles": [
            {
                "frequency": {
                    "interval_unit": "DAY",
                    "interval_count": 1
                },
                "tenure_type": "REGULAR",
                "sequence": 1,
                "total_cycles": 0,   
                "pricing_scheme": {
                    "fixed_price": {
                        "value": "21",
                        "currency_code": "USD"
                    }
                }
            }
        ],
        "payment_preferences": {
            "auto_bill_outstanding": True,
            "payment_failure_threshold": 3
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print('create_plan:', response.json())
    return response.json()


def create_subscription():
    url = 'https://api-m.sandbox.paypal.com/v1/billing/subscriptions'
    headers = {
        "Content-Type": "application/json",
        "Authorization": authorization,
        "PayPal-Request-Id": str(uuid.uuid4())
    }
    data = {
        "plan_id": "P-8MN77060VY799034YMDWT3JY",
        "shipping_amount": {
            "currency_code": "USD",
            "value": "10.00"
        },
        "subscriber": {
            "name": {
                "given_name": "Jordan",
                "surname": "Borja"
            },
            "email_address": "jb@example.com",
            "shipping_address": {
                "name": {
                    "full_name": "Jordano Borjano"
                },
                "address": {
                    "address_line_1": "2211 N First Street",
                    "address_line_2": "Building 17",
                    "admin_area_2": "San Jose",
                    "admin_area_1": "CA",
                    "postal_code": "95131",
                    "country_code": "US"
                }
            }
        },
        "application_context": {
            "brand_name": "Cheesy Bittes",
            "locale": "en-US",
            "shipping_preference": "SET_PROVIDED_ADDRESS",
            "user_action": "SUBSCRIBE_NOW",
            "payment_method": {
                "payer_selected": "PAYPAL",
                "payee_preferred": "IMMEDIATE_PAYMENT_REQUIRED"
            },
            "return_url": "https://cheesybittes.netlify.app/checkout",
            "cancel_url": "https://cheesybittes.netlify.app/checkout"
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print('create_subscription:', response.json())
    return response.json()


def show_subscription_details():
    url = 'https://api-m.sandbox.paypal.com/v1/billing/subscriptions/I-S39436D0F2AF'
    headers = {
        "Content-Type": "application/json",
        "Authorization": authorization,
    }
    response = requests.get(url, headers=headers)
    print('show_subscription_details:', response.json())
    return response.json()


def activate_subscription():
    url = 'https://api-m.sandbox.paypal.com/v1/billing/subscriptions/I-S39436D0F2AF/activate'
    headers = {
        "Content-Type": "application/json",
        "Authorization": authorization,
    }
    data = {
        'reason': 'Activating subscription by Jordan'
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print('activate_subscription:', response.json())
    return response.json()
