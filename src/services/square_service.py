from ..db.documents import SquarePaymentError, Order

from .checkout_service import get_checkout_contact

from square.client import Client

from decouple import config

from datetime import datetime
from decimal import Decimal
import uuid
import math


client = Client(
    access_token=config('SQUARE_ACCESS_TOKEN'), 
    environment=config('SQUARE_ENVIRONMENT')
)

# PAYMENTS

def list_payments():
    result = client.payments.list_payments()

    if result.is_success():
        return result.body
    elif result.is_error():
        print(result.errors)
        raise Exception('Error in list_payments: {}'.format(result.errors[0].get('detail')))


def to_payment_object(data):
    card_details = data.get('card_details', {})
    card_payment_timeline = card_details.get('card_payment_timeline', {})
    datetime_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    datetime_default = "2000-01-01T00:00:00.0Z"
    
    def to_datetime(key_from, key): 
        date_time = key_from.get(key, datetime_default)
        return datetime.strptime(date_time, datetime_format)

    return {
        "payment_id": data.get('id'),
        "status": data.get('status'),
        "source_type": data.get('source_type'),
        "amount_money": data.get('amount_money', {}).get('amount'),
        "tip_money": Decimal(data.get('tip_money', {}).get('amount', -100)),
        "approved_money": Decimal(data.get('approved_money').get('amount', -100)),
        "total_money": Decimal(data.get('total_money', {}).get('amount', -100)),
        "fee_money": Decimal(data.get('app_fee_money', {}).get('amount', -100)),
        "avs_status": card_details.get('avs_status'),
        "card": card_details.get('card'),
        "card_status": card_details.get('status'),
        "card_error": card_details.get('errors'),
        "created_at": to_datetime(data, 'created_at'),
        "authorized_at": to_datetime(card_payment_timeline, 'authorized_at'),
        "captured_at": to_datetime(card_payment_timeline, 'captured_at'),
        "voided_at": to_datetime(card_payment_timeline, 'voided_at'),
        "updated_at": to_datetime(data, 'updated_at'),
        "cvv_status": card_details.get('cvv_status'),
        "entry_method": card_details.get('entry_method'),
        "statement_description": card_details.get('statement_description'),
        "verification_method": card_details.get('verification_method'),
        "verification_results": card_details.get('verification_results'),
        "delay_action": data.get('delay_action'),
        "delay_duration": data.get('delay_duration'),
        "delayed_until": to_datetime(data, 'delayed_until'),
        "order_id": data.get('order_id'),
        "location_id": data.get('location_id'),
        "receipt_number": data.get('receipt_number'),
        "risk_evaluation": data.get('risk_evaluation'),
        "buyer_email_address": data.get('buyer_email_address'),
        "billing_address": data.get('billing_address'),
        "shipping_address": data.get('shipping_address'),
        "note": data.get('note'),
        "version_token": data.get('version_token')
    }


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
            "choose1": item.choose1,
            "choose3": item.choose3
        }
        new_cart.append(new_item)
    
    return new_cart


def create_payment(payment_token, amount, cart, id):

    print('Cart:', type(cart), cart)

    contact = get_checkout_contact(id)
    shipping = contact.shipping_information
    billing = contact.billing_information

    idempotency_key = str(uuid.uuid4())
    amount = math.trunc(amount)

    body = {
        "source_id": payment_token,
        "idempotency_key": idempotency_key,
        "amount_money": {
            "amount": amount,
            "currency": "USD"
        },
        "buyer_email_address": billing.email,
        "shipping_address": {
            "address_line_1": shipping.address,
            "address_line_2": shipping.address2,
            "city": shipping.city,
            "state_or_province": shipping.state,
            "postal_code": shipping.zip_code,
            "country": "US",
            "first_name": shipping.name,
        },
        "billing_address": {
            "address_line_1": billing.address,
            "address_line_2": billing.address2,
            "city": billing.city,
            "state_or_province": billing.state,
            "postal_code": billing.zip_code,
            "country": "US",
            "first_name": billing.name,
        },
    }
    result = client.payments.create_payment(body=body)
    
    if result.is_success():
        order = Order(
            cart=to_cart_object(cart), 
            square=to_payment_object(result.body['payment']), 
            checkout_info=contact.to_json()
        ).save()
        
        return order.square.status

    elif result.is_error():
        for error in result.errors:
            SquarePaymentError(
                category = error.get('category'),
                code = error.get('code'),
                detail = error.get('detail'),
                field = error.get('field'),
                payment_token = payment_token,
                amount = amount,
                idempotency_key = idempotency_key
            ).save()
        raise Exception('Error in create_payment: {}'.format(result.errors[0].get('detail')))


# CUSTOMERS

def list_customers():
    result = client.customers.list_customers()

    if result.is_success():
        return result.body
    elif result.is_error():
        print(result.errors)
        raise Exception('Error in list_customers: {}'.format(result.errors[0].get('detail')))


def create_customer():
    result = client.customers.create_customer(
        body = {
            "given_name": "Customer",
            "family_name": "New",
            "email_address": "customer@cheesybittes.com",
            "address": {
                "address_line_1": "501 Electric Ave",
                "address_line_2": "Suite 601",
                "locality": "New Yorke",
                "postal_code": "10004",
                "country": "US"
            },
            "phone_number": "8945123156",
            "note": "New Customer (2)",
        }
    )

    if result.is_success():
        print(result.body)
    elif result.is_error():
        print(result.errors)
        raise Exception('Error in create_customer: {}'.format(result.errors[0].get('detail')))


# CARDS

def list_cards():
    result = client.cards.list_cards()

    if result.is_success():
        print(result.body)
    elif result.is_error():
        print(result.errors)
        raise Exception('Error in list_cards: {}'.format(result.errors[0].get('detail')))


def create_card():
    idempotency_key = str(uuid.uuid4())
    result = client.cards.create_card(
        body = {
            "idempotency_key": idempotency_key,
            "source_id": "cnon:CBASEHGhk86Wu5B7M6pcF7fax7o",
            "card": {
                "cardholder_name": "Jordano Borjano",
                "customer_id": "JDPSX0F8MCXYX6WTF8D9VGVAGW",
            }
        }
    )

    if result.is_success():
        print(result.body)
    elif result.is_error():
        print(result.errors)
        raise Exception('Error in create_card: {}'.format(result.errors[0].get('detail')))


# CATALOGS

def get_catalog_info():
    result = client.catalog.catalog_info()

    if result.is_success():
        print(result.body)
    elif result.is_error():
        print(result.errors)
        raise Exception('Error in get_catalog_info.: {}'.format(result.errors[0].get('detail')))


def list_catalogs():
    result = client.catalog.list_catalog(types = "SUBSCRIPTION_PLAN")

    if result.is_success():
        return result.body
    elif result.is_error():
        print('Error:', result.errors)
        raise Exception('Error in list_catalogs: {}'.format(result.errors[0].get('detail')))


def upsert_catalog():
    idempotency_key = str(uuid.uuid4())
    result = client.catalog.upsert_catalog_object(
        body = {
            "idempotency_key": idempotency_key,
            "object": {
                "type": "SUBSCRIPTION_PLAN",
                "id": "#plan5",
                "subscription_plan_data": {
                    "name": "Cheesy Bittes Club..",
                    "phases": [
                        {
                            "cadence": "DAILY",
                            "recurring_price_money": {
                                "amount": 1500,
                                "currency": "USD"
                            }
                        }
                    ]
                }
            }
        }
    )

    if result.is_success():
        print('Result:', result.body)
    elif result.is_error():
        print('Error:', result.errors)
        raise Exception('Error in upsert_catalog: {}'.format(result.errors[0].get('detail')))


# SUBSCRIPTIONS

def create_subscription():
    idempotency_key = str(uuid.uuid4())
    result = client.subscriptions.create_subscription(
        body = {
            "idempotency_key": idempotency_key,
            "location_id": "LWB5K8RGJYJSY",
            "plan_id": "SIEONDW43O4OGA4KQGCD6VAL",
            "customer_id": "JDPSX0F8MCXYX6WTF8D9VGVAGW",
            "card_id": "ccof:sQ7T97tS3qWMafDg4GB",
            "tax_percentage": "5",
        }
    )

    if result.is_success():
        print('Result:', result.body)
    elif result.is_error():
        print('Error:', result.errors)
        raise Exception('Error in create_subscription: {}'.format(result.errors[0].get('detail')))


def init_subscription():
    pass


# INVOICES

def list_invoices():
    result = client.invoices.list_invoices(location_id = "LWB5K8RGJYJSY")

    if result.is_success():
        return result.body
    elif result.is_error():
        print(result.errors)
        raise Exception('Error in list_invoices: {}'.format(result.errors[0].get('detail')))

