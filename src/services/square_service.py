from square.client import Client

from decouple import config

import uuid


client = Client(access_token=config('SQUARE_ACCESS_TOKEN'), environment='sandbox')

def create_payment(payment_token):
    body = {
        "source_id": payment_token,
        "idempotency_key": str(uuid.uuid4()),
        "amount_money": {
            "amount": 2,
            "currency": "USD"
        }
    }
    result = client.payments.create_payment(body=body)
    
    if result.is_success():
        print('Sucess:', result.body)
    elif result.is_error():
        print('Square Error:', result.errors)
