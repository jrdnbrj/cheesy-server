from graphene.types.scalars import String
from mongoengine.document import Document
from mongoengine.fields import (
    StringField,
    DecimalField,
    DictField,
    DateTimeField
)

from datetime import datetime


class Product(Document):
    name = StringField(required=True, unique=True, max_length=25)
    images = StringField(max_length=1000)
    description = StringField(required=True, max_length=1000)
    short_description = StringField(max_length=500)
    ingredients = StringField(required=True, max_length=500)
    price = DecimalField(precision=2)
    path = StringField(max_length=15)


class PayPalOrder(Document):
    order_id = StringField()
    status = StringField()
    value = DecimalField(precision=2)
    name = StringField()
    surname = StringField()
    full_name = StringField()
    payer_id = StringField()
    email = StringField()
    address = DictField()
    capture_id  = StringField()
    capture_status = StringField()
    purchase_breakdown = DictField()
    capture_time = DateTimeField(default=datetime.utcnow)
    create_time = DateTimeField()
    update_time = DateTimeField()


class SquarePayment(Document): # https://developer.squareup.com/reference/square/objects/Payment
    payment_id = StringField() # A unique ID for the payment, given by Square
    status = StringField() # APPROVED, PENDING, COMPLETED, CANCELED, or FAILED.
    source_type = StringField() # CARD, BANK_ACCOUNT, CASH, or EXTERNAL
    amount_money = DecimalField(precision=2) # The amount processed for this payment, not including tip_money
    tip_money = DecimalField(precision=2)
    approved_money = DecimalField(precision=2)
    total_money = DecimalField(precision=2) # is the sum of amount_money and tip_money
    fee_money = DecimalField(precision=2)
    avs_status = StringField() # AVS_ACCEPTED, AVS_REJECTED, or AVS_NOT_CHECKED
    card = DictField() # The credit card's non-confidential details
    card_status = StringField() # AUTHORIZED, CAPTURED, VOIDED, or FAILED
    card_error = DictField() # Information about errors encountered during the request, return an array of dicts
    created_at = DateTimeField() # when the payment was created
    authorized_at = DateTimeField() # when the payment was authorized
    captured_at = DateTimeField() # when the payment was captured
    voided_at = DateTimeField() # when the payment was voided
    updated_at = DateTimeField() # when the payment was last updated
    cvv_status = StringField() # CVV_ACCEPTED, CVV_REJECTED, or CVV_NOT_CHECKED
    entry_method = StringField() # KEYED, SWIPED, EMV, ON_FILE, or CONTACTLESS
    statement_description = StringField()
    verification_method = StringField() # PIN, SIGNATURE, PIN_AND_SIGNATURE, ON_DEVICE, or NONE
    verification_results = StringField() # SUCCESS, FAILURE, or UNKNOWN
    delay_action = StringField() # The action to be applied to the payment when the delay_duration has elapsed.
    delay_duration = StringField() # The duration of time after the payment's creation when Square automatically applies the delay_action to the payment
    delay_until = DecimalField(precision=2) # when the delay_action is automatically applied
    order_id = StringField()
    location_id = StringField()
    receipt_number = StringField() # The payment's receipt number. The field is missing if a payment is canceled.
    risk_evaluation = DictField() # Provides information about the risk associated with the payment, as determined by Square.
    buyer_email_address = StringField()
    billing_address = StringField()
    shipping_address = StringField()
    note = StringField() # An optional note to include when creating a payment.
    version_token = StringField() # Used for optimistic concurrency. This opaque token identifies a specific version of the Payment object.
