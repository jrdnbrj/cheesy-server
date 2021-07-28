from ..db.documents import SquarePaymentError, Order, Subscription

from .checkout_service import get_checkout_contact

from square.client import Client
from decouple import config

from dateutil.relativedelta import relativedelta
from datetime import datetime, date
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


def create_payment(payment_token, amount, contact_id, cart, shipping_value, discount):

    print('Cart:', type(cart), cart)

    if not validate_amount(cart, shipping_value, discount, amount):
        raise Exception("Amount does not match with Cart's items")

    checkout, subscription = checkout_subscription(cart)

    contact = get_checkout_contact(contact_id)
    shipping = contact.shipping_information
    billing = contact.billing_information

    idempotency_key = str(uuid.uuid4())
    amount = math.trunc(amount * 100)

    customer_id = create_customer(billing)
    card_id = create_card(payment_token, customer_id)

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
        },
    }
    result = client.payments.create_payment(body=body)
    
    if result.is_success():
        order = Order(
            cart=to_cart_object(checkout + subscription), 
            square=to_payment_object(result.body['payment']), 
            checkout_info=contact.to_json()
        ).save()

        if subscription != []:
            init_subscription(payment_token, subscription, shipping, contact, customer_id, card_id)

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


def create_customer(billing):
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
        print(result.body, type(result.body))
        print('ID:', result.body['customer']['id'])
        return result.body['customer']['id']
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


def create_card(payment_token, customer_id):
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
        print(result.body)
        print('Card ID:', result.body['card']['id'])
        return result.body['card']['id']
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


def upsert_catalog(cadence, amount):
    idempotency_key = str(uuid.uuid4())
    plan_object_id = '#{}'.format(str(uuid.uuid4()))
    print('plan_object_id:', plan_object_id)

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
        print('Result:', result.body)
        print('Catalog ID:', result.body['catalog_object']['id'])
        return result.body['catalog_object']['id']
    elif result.is_error():
        print('Error:', result.errors)
        raise Exception('Error in upsert_catalog: {}'.format(result.errors[0].get('detail')))


# SUBSCRIPTIONS

def create_subscription(plan_id, customer_id, card_id, interval):
    idempotency_key = str(uuid.uuid4())

    today = date.today()
    # start_date = today + relativedelta(months=interval)
    start_date = today + relativedelta(days=interval)

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
        print('Result:', result.body)
        return result.body
    elif result.is_error():
        print('Error:', result.errors)
        raise Exception('Error in create_subscription: {}'.format(result.errors[0].get('detail')))


def init_subscription(payment_token, cart, shipping, contact, customer_id, card_id):
    print('Init Subscription.')
    monthly, two_months = monthly_two_months(cart)
    
    print('Monthly:', monthly)
    print('Two Months:', two_months)
    
    try:
        if monthly:
            plan_id = upsert_catalog('DAILY', 230) # MONTHLY
            subscription = create_subscription(plan_id, customer_id, card_id, 1)
            Order(
                type="SUBSCRIPTION",
                cart=to_cart_object(cart), 
                square=to_subscription_object(subscription, contact.billing_information.email, 230), 
                checkout_info=contact.to_json()
            ).save()

        if two_months:
            plan_id = upsert_catalog('DAILY', 1242) # EVERY_TWO_MONTHS
            subscription = create_subscription(plan_id, customer_id, card_id, 2)
            Order(
                type="SUBSCRIPTION",
                cart=to_cart_object(cart), 
                square=to_subscription_object(subscription, contact.billing_information.email, 1242), 
                checkout_info=contact.to_json()
            ).save()
    except:
        raise Exception('Error in init_subscription.')



# INVOICES

def list_invoices():
    result = client.invoices.list_invoices(location_id = "LWB5K8RGJYJSY")

    if result.is_success():
        return result.body
    elif result.is_error():
        print(result.errors)
        raise Exception('Error in list_invoices: {}'.format(result.errors[0].get('detail')))


# UTILS

def validate_amount(cart, shipping, discount, amount):
    subtotal = 0
    
    for item in cart:
        price = round(Decimal(item['price']), 2)
        quantity = round(Decimal(item['amount']), 2)
        subtotal += price * quantity

    shipping = round(Decimal(shipping), 2)
    discount = round(Decimal(discount), 2)
    total = subtotal + shipping - discount

    if total != round(Decimal(amount), 2):
        print('Amount does not match: {} != {}'.format(total, round(Decimal(amount), 2)))
        return False

    return True


def checkout_subscription(cart):
    checkout = []
    subscription = []

    for item in cart:
        if item.join_club:
            subscription.append(item)
        else:
            checkout.append(item)

    return checkout, subscription


def to_subscription_object(data, email, amount):
    return {
        "created_at": datetime.strptime(data.get('created_at', '2000-01-01T00:00:00.0Z'), '%Y-%m-%dT%H:%M:%S.%fZ'),
        "status": data.get('status'),
        "buyer_email_address": email,
        "subscription_id": data.get('id'),
        "total_money": amount,
        "start_date": datetime.strptime(data.get('start_date', '2000-01-01'), '%Y-%m-%d'),
    }


def to_payment_object(data):
    # card_details = data.get('card_details', {})
    # card_payment_timeline = card_details.get('card_payment_timeline', {})
    datetime_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    datetime_default = "2000-01-01T00:00:00.0Z"
    
    def to_datetime(key_from, key): 
        date_time = key_from.get(key, datetime_default)
        return datetime.strptime(date_time, datetime_format)

    return {
        "payment_id": data.get('id'),
        "status": data.get('status'),
        "total_money": Decimal(data.get('total_money', {}).get('amount', -100)),
        "created_at": to_datetime(data, 'created_at'),
        "buyer_email_address": data.get('buyer_email_address'),
    }

    # return {
    #     "payment_id": data.get('id'),
    #     "status": data.get('status'),
    #     "source_type": data.get('source_type'),
    #     "amount_money": data.get('amount_money', {}).get('amount'),
    #     "tip_money": Decimal(data.get('tip_money', {}).get('amount', -100)),
    #     "approved_money": Decimal(data.get('approved_money').get('amount', -100)),
    #     "total_money": Decimal(data.get('total_money', {}).get('amount', -100)),
    #     "fee_money": Decimal(data.get('app_fee_money', {}).get('amount', -100)),
    #     "avs_status": card_details.get('avs_status'),
    #     "card": card_details.get('card'),
    #     "card_status": card_details.get('status'),
    #     "card_error": card_details.get('errors'),
    #     "created_at": to_datetime(data, 'created_at'),
    #     "authorized_at": to_datetime(card_payment_timeline, 'authorized_at'),
    #     "captured_at": to_datetime(card_payment_timeline, 'captured_at'),
    #     "voided_at": to_datetime(card_payment_timeline, 'voided_at'),
    #     "updated_at": to_datetime(data, 'updated_at'),
    #     "cvv_status": card_details.get('cvv_status'),
    #     "entry_method": card_details.get('entry_method'),
    #     "statement_description": card_details.get('statement_description'),
    #     "verification_method": card_details.get('verification_method'),
    #     "verification_results": card_details.get('verification_results'),
    #     "delay_action": data.get('delay_action'),
    #     "delay_duration": data.get('delay_duration'),
    #     "delayed_until": to_datetime(data, 'delayed_until'),
    #     "order_id": data.get('order_id'),
    #     "location_id": data.get('location_id'),
    #     "receipt_number": data.get('receipt_number'),
    #     "risk_evaluation": data.get('risk_evaluation'),
    #     "buyer_email_address": data.get('buyer_email_address'),
    #     "billing_address": data.get('billing_address'),
    #     "shipping_address": data.get('shipping_address'),
    #     "note": data.get('note'),
    #     "version_token": data.get('version_token')
    # }


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


def monthly_two_months(cart):
    monthly = []
    two_months = []

    for item in cart:
        if item.interval == 1:
            monthly.append(item)
        elif item.interval == 2:
            two_months.append(item)
        
    return monthly, two_months
