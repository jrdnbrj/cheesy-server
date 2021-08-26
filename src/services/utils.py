from decimal import Decimal
from datetime import datetime


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
        # "purchase_breakdown": order['purchase_units'][0]['payments']['captures'][0]['seller_receivable_breakdown'],
        "create_time": datetime.strptime(order['purchase_units'][0]['payments']['captures'][0]['create_time'], "%Y-%m-%dT%H:%M:%SZ"),
        "update_time": datetime.strptime(order['purchase_units'][0]['payments']['captures'][0]['update_time'], "%Y-%m-%dT%H:%M:%SZ"),
    }


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
        "created_at": datetime.strptime(data.get('created_at', '2000-01-01T00:00:00.0Z'), '%Y-%m-%dT%H:%M:%SZ'),
        "status": data.get('status'),
        "buyer_email_address": email,
        "subscription_id": data.get('id'),
        "total_money": amount,
        "start_date": datetime.strptime(data.get('start_date', '2000-01-01'), '%Y-%m-%d'),
    }


def to_payment_object(data):
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


def monthly_two_months(cart):
    monthly = []
    two_months = []

    for item in cart:
        if item.interval == 1:
            monthly.append(item)
        elif item.interval == 2:
            two_months.append(item)
        
    return monthly, two_months

