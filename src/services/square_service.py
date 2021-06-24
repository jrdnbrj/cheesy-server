from ..db.documents import SquarePayment, SquarePaymentError

from square.client import Client

from decouple import config

from datetime import datetime
from decimal import Decimal
import uuid


client = Client(
    access_token=config('SQUARE_ACCESS_TOKEN'), 
    environment=config('SQUARE_ENVIRONMENT')
)


def create_payment(payment_token, amount):
    idempotency_key = str(uuid.uuid4())

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

    elif result.is_error():
        # print('Square Error:', result.errors)
        
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



