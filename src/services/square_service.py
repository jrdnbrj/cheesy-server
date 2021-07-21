from ..db.documents import SquarePayment, SquarePaymentError

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


def create_payment(payment_token, amount):
    idempotency_key = str(uuid.uuid4())
    amount = math.trunc(amount)

    body = {
        "source_id": payment_token,
        "idempotency_key": idempotency_key,
        "amount_money": {
            "amount": amount,
            "currency": "USD"
        }
    }
    result = client.payments.create_payment(body=body)
    
    if result.is_success():
        data = result.body['payment']
        
        card_details = data.get('card_details', {})
        card_payment_timeline = card_details.get('card_payment_timeline', {})
        datetime_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        datetime_default = "2000-01-01T00:00:00.0Z"
        
        def to_datetime(key_from, key): 
            date_time = key_from.get(key, datetime_default)
            return datetime.strptime(date_time, datetime_format)

        new_payment = SquarePayment(
            payment_id = data.get('id'),
            status = data.get('status'),
            source_type = data.get('source_type'),
            amount_money = data.get('amount_money', {}).get('amount'),
            tip_money = Decimal(data.get('tip_money', {}).get('amount', -100)),
            approved_money = Decimal(data.get('approved_money').get('amount', -100)),
            total_money = Decimal(data.get('total_money', {}).get('amount', -100)),
            fee_money = Decimal(data.get('app_fee_money', {}).get('amount', -100)),
            avs_status = card_details.get('avs_status'),
            card = card_details.get('card'),
            card_status = card_details.get('status'),
            card_error = card_details.get('errors'),
            created_at = to_datetime(data, 'created_at'),
            authorized_at = to_datetime(card_payment_timeline, 'authorized_at'),
            captured_at = to_datetime(card_payment_timeline, 'captured_at'),
            voided_at = to_datetime(card_payment_timeline, 'voided_at'),
            updated_at = to_datetime(data, 'updated_at'),
            cvv_status = card_details.get('cvv_status'),
            entry_method = card_details.get('entry_method'),
            statement_description = card_details.get('statement_description'),
            verification_method = card_details.get('verification_method'),
            verification_results = card_details.get('verification_results'),
            delay_action = data.get('delay_action'),
            delay_duration = data.get('delay_duration'),
            delayed_until = to_datetime(data, 'delayed_until'),
            order_id = data.get('order_id'),
            location_id = data.get('location_id'),
            receipt_number = data.get('receipt_number'),
            risk_evaluation = data.get('risk_evaluation'),
            buyer_email_address = data.get('buyer_email_address'),
            billing_address = data.get('billing_address'),
            shipping_address = data.get('shipping_address'),
            note = data.get('note'),
            version_token = data.get('version_token')
        )
        new_payment.save()

        return data.get('status')
    elif result.is_error():
        for error in result.errors:
            new_payment_error = SquarePaymentError(
                category = error.get('category'),
                code = error.get('code'),
                detail = error.get('detail'),
                field = error.get('field'),
                payment_token = payment_token,
                amount = amount,
                idempotency_key = idempotency_key
            )
            new_payment_error.save()
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


# INVOICES

def list_invoices():
    result = client.invoices.list_invoices(location_id = "LWB5K8RGJYJSY")

    if result.is_success():
        return result.body
    elif result.is_error():
        print(result.errors)
        raise Exception('Error in list_invoices: {}'.format(result.errors[0].get('detail')))

