from ..db.documents import SquarePaymentError, Order

from .checkout_service import get_checkout_contact

from .utils import (
    monthly_two_months, 
    to_payment_object, 
    to_subscription_object, 
    checkout_subscription, 
    validate_amount, 
    to_cart_object
)

from square.client import Client
from decouple import config

from dateutil.relativedelta import relativedelta
from datetime import date
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
        raise Exception('Error in list_payments: {}'.format(result.errors[0]))


def get_payment(payment_id):
    print('asd')
    result = client.payments.get_payment(payment_id=payment_id)

    if result.is_success():
        print(result.body['payment'])
        return result.body['payment']
    elif result.is_error():
        print(result.errors)


def create_payment(payment_token, amount, contact_id, cart, shipping_value, discount):

    if not validate_amount(cart, shipping_value, discount, amount):
        raise Exception("Amount does not match with Cart's items")

    checkout, subscription = checkout_subscription(cart)

    contact = get_checkout_contact(contact_id)
    shipping = contact.shipping_information
    billing = contact.billing_information

    idempotency_key = str(uuid.uuid4())
    amount = math.trunc(amount * 100)

    customer_id = create_customer(billing, amount)
    card_id = create_card(payment_token, customer_id, amount)

    body = {
        "source_id": card_id,
        "customer_id": customer_id,
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
        }
    }
    result = client.payments.create_payment(body=body)
    
    if result.is_success():
        order = Order(
            cart=to_cart_object(checkout + subscription), 
            square=to_payment_object(result.body['payment']), 
            checkout_info=contact.to_json()
        ).save()

        if subscription != []:
            response = init_subscription(subscription, shipping_value, contact, customer_id, card_id)

            if not response:
                return 'An error has occurred with Square Server. The first payment has been completed successfully but the Cheesy Bittes Club subscriptions may not have been generated. Please Contact Us'

        if order.square.status != 'COMPLETED':
            return 'An error may have occurred with your order, please contact us. Status: '.format(order.square.status)

        return order.square.status

    elif result.is_error():
        for error in result.errors:
            print('Error in create_payment: ', error)
            SquarePaymentError(
                category = error.get('category'),
                code = error.get('code'),
                detail = error.get('detail'),
                field = error.get('field'),
                customer_id = customer_id,
                card_id = card_id,
                amount = amount / 100,
                type = 'ONCE'
            ).save()
        return 'An error has occurred. No payment has been made. Please try again.'


# CUSTOMERS

def create_customer(billing, amount):
    result = client.customers.create_customer(
        body = {
            "given_name": billing.name,
            "email_address": billing.email,
            "address": {
                "first_name": billing.name,
                "address_line_1": billing.address,
                "address_line_2": billing.address2,
                "locality": billing.city,
                "sublocality": billing.state,
                "postal_code": billing.zip_code,
                "country": "US",
            },
            "phone_number": billing.phone,
        }
    )

    if result.is_success():
        print('Customer ID:', result.body['customer']['id'])
        return result.body['customer']['id']
    elif result.is_error():
        for error in result.errors:
            print('Error in create_customer: ', error)
            SquarePaymentError(
                category = error.get('category'),
                code = error.get('code'),
                detail = error.get('detail'),
                field = error.get('field'),
                amount = amount / 100,
                type = 'CREATE_CUSTOMER'
            ).save()
        raise Exception('An error has occurred. No payment has been made.')


# CARDS

def create_card(payment_token, customer_id, amount):
    idempotency_key = str(uuid.uuid4())
    result = client.cards.create_card(
        body = {
            "idempotency_key": idempotency_key,
            "source_id": payment_token,
            "card": {
                "customer_id": customer_id,
            }
        }
    )

    if result.is_success():
        print('Card ID:', result.body['card']['id'])
        return result.body['card']['id']
    elif result.is_error():
        for error in result.errors:
            print('Error in create_card: ', error)
            SquarePaymentError(
                category = error.get('category'),
                code = error.get('code'),
                detail = error.get('detail'),
                field = error.get('field'),
                amount = amount / 100,
                type = 'CREATE_CARD'
            ).save()
        raise Exception('An error has occurred. No payment has been made.')


# CATALOGS

def retrieve_catalog(catalog_id):
    result = client.catalog.retrieve_catalog_object(object_id=catalog_id)

    if result.is_success():
        print(result.body['object'])
        return result.body['object']
    elif result.is_error():
        print(result.errors)
        raise Exception('Error in retrieve_catalog: {}'.format(result.errors[0]))


def upsert_catalog(cadence, amount, customer_id, card_id):
    idempotency_key = str(uuid.uuid4())
    plan_object_id = '#{}'.format(str(uuid.uuid4()))

    result = client.catalog.upsert_catalog_object(
        body = {
            "idempotency_key": idempotency_key,
            "object": {
                "type": "SUBSCRIPTION_PLAN",
                "id": plan_object_id,
                "subscription_plan_data": {
                    "name": "Cheesy Bittes Club.",
                    "phases": [
                        {
                            "cadence": cadence,
                            "recurring_price_money": {
                                "amount": amount,
                                "currency": "USD"
                            }
                        }
                    ]
                }
            }
        }
    )

    if result.is_success():
        print('Plan ID:', result.body['catalog_object']['id'])
        return result.body['catalog_object']['id']
    elif result.is_error():
        for error in result.errors:
            print('Error in upsert_catalog: ', error)
            SquarePaymentError(
                category = error.get('category'),
                code = error.get('code'),
                detail = error.get('detail'),
                field = error.get('field'),
                amount = amount / 100,
                customer_id = customer_id,
                card_id = card_id,
                type = 'CREATE_PLAN'
            ).save()
        raise Exception('An error has occurred. No payment has been made.')


# SUBSCRIPTIONS

def create_subscription(plan_id, customer_id, card_id, interval, amount):
    idempotency_key = str(uuid.uuid4())

    start_date = date.today() + relativedelta(months=interval)

    result = client.subscriptions.create_subscription(
        body = {
            "idempotency_key": idempotency_key,
            "location_id": "LWB5K8RGJYJSY",
            "plan_id": plan_id,
            "customer_id": customer_id,
            "card_id": card_id,
            "start_date": start_date
            # "tax_percentage": "5",
        }
    )

    if result.is_success():
        print('Subscription ID:', result.body['subscription']['id'])
        return result.body['subscription']
    elif result.is_error():
        for error in result.errors:
            print('Error in create_subscription: ', error)
            SquarePaymentError(
                category = error.get('category'),
                code = error.get('code'),
                detail = error.get('detail'),
                field = error.get('field'),
                amount = amount / 100,
                customer_id = customer_id,
                card_id = card_id,
                type = 'SUBSCRIPTION',
            ).save()
        raise Exception('An error has occurred. No payment has been made.')


def retrieve_subscription(subscription_id):
    result = client.subscriptions.retrieve_subscription(subscription_id=subscription_id)

    if result.is_success():
        print(result.body['subscription'])
        catalog = retrieve_catalog(result.body['subscription']['plan_id'])
        result = result.body['subscription']
        result['plan'] = catalog
        return result
    elif result.is_error():
        print(result.errors)
        raise Exception('Error in retrieve_subscription: {}'.format(result.errors[0]))


def cancel_subscription(subscription_id):
    result = client.subscriptions.cancel_subscription(subscription_id=subscription_id)

    if result.is_success():
        print('Subscription Status:', result.body['subscription']['status'])
        return result.body['subscription']['status']
    elif result.is_error():
        for error in result.errors:
            print('Error in cancel_subscription: ', error)
            SquarePaymentError(
                category = error.get('category'),
                code = error.get('code'),
                detail = error.get('detail'),
                field = error.get('field'),
                type = 'SUBSCRIPTION',
            ).save()
        raise Exception('An error has occurred. The subscription has not been canceled.')


def init_subscription(cart, shipping_value, contact, customer_id, card_id):
    monthly, two_months = monthly_two_months(cart)
    
    try:
        if monthly != []:
            subtotal = 0
            for item in monthly:
                price = round(Decimal(item['price']), 2)
                quantity = round(Decimal(item['amount']), 2)
                subtotal += price * quantity

            total = subtotal + round(Decimal(shipping_value), 2)
            total = math.trunc(total * 100)

            plan_id = upsert_catalog('MONTHLY', total, customer_id, card_id)
            subscription = create_subscription(plan_id, customer_id, card_id, 1, total)

            Order(
                type="SUBSCRIPTION",
                cart=to_cart_object(monthly), 
                square=to_subscription_object(subscription, contact.billing_information.email, total), 
                checkout_info=contact.to_json()
            ).save()

        if two_months != []:
            subtotal = 0
            for item in two_months:
                price = round(Decimal(item['price']), 2)
                quantity = round(Decimal(item['amount']), 2)
                subtotal += price * quantity

            total = subtotal + round(Decimal(shipping_value), 2)
            total = math.trunc(total * 100)

            plan_id = upsert_catalog('EVERY_TWO_MONTHS', total, customer_id, card_id)
            subscription = create_subscription(plan_id, customer_id, card_id, 2, total)

            Order(
                type="SUBSCRIPTION",
                cart=to_cart_object(two_months), 
                square=to_subscription_object(subscription, contact.billing_information.email, total), 
                checkout_info=contact.to_json()
            ).save()

        return True
    except Exception as e:
        print('Error in init_subscription:', e)
        SquarePaymentError(
            detail = str(e),
            amount = total / 100,
            customer_id = customer_id,
            card_id = card_id,
            type = 'SUBSCRIPTION',
        ).save()
        return False



# INVOICES

def list_invoices():
    result = client.invoices.list_invoices(location_id = "LWB5K8RGJYJSY")

    if result.is_success():
        return result.body
    elif result.is_error():
        print(result.errors)
        raise Exception('Error in list_invoices: {}'.format(result.errors[0]))


# ERRORS

def list_square_errors():
    return SquarePaymentError.objects()
