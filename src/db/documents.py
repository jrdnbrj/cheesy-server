from mongoengine.document import Document, EmbeddedDocument
from mongoengine.fields import (
    StringField,
    DecimalField,
    DictField,
    BooleanField,
    DateTimeField,
    ListField,
    EmailField,
    IntField,
    EmbeddedDocumentField,
    EmbeddedDocumentListField
)

from datetime import datetime


class Product(Document):
    name = StringField(required=True, max_length=25)
    images = ListField(max_length=1000)
    smoothies = ListField()
    description = StringField(required=True, max_length=1000)
    short_description = StringField(max_length=500)
    ingredients = ListField(required=True, max_length=500)
    price = DecimalField(precision=2)
    path = StringField(max_length=15)
    sequence = IntField()


class Cart(EmbeddedDocument):
    amount = IntField(required=True)
    price = DecimalField(required=True)
    name = StringField()
    total = DecimalField(required=True)
    bundle_up = IntField()
    buy_once = BooleanField()
    join_club = BooleanField()
    interval = IntField()
    choose1 = StringField()
    choose3 = ListField(ListField())

    def to_json(self):
        return {
            "amount": self.amount,
            "price": self.price,
            "name": self.name,
            "total": self.total,
            "bundle_up": self.bundle_up,
            "buy_once": self.buy_once,
            "join_club": self.join_club,
            "interval": self.interval,
            "choose1": self.choose1,
            "choose3": self.choose3
        }


class Contact(Document):
    full_name = StringField()
    email = EmailField()
    phone = StringField()
    message = StringField()


class Home(Document):
    name = StringField()
    description = StringField()
    sequence = IntField()


class OurFamily(Document):
    title = StringField()
    description = StringField()
    sequence = IntField()


class Coupon(Document):
    code = StringField(max_length=10, unique=True)
    discount = StringField()
    is_active = BooleanField(default=True)


class Settings(Document):
    discount_month = DecimalField(precision=1)
    discount_2months = DecimalField(precision=1)
    password = StringField()


class CheckoutInfoEmbedded(EmbeddedDocument):
    name = StringField()
    phone = StringField()
    email = StringField()
    address = StringField()
    address2 = StringField()
    city = StringField()
    state = StringField()
    zip_code = StringField()

    def to_json(self):
        return {
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
            "address2": self.address2,
            "city": self.city,
            "state": self.state,
            "zip_code": self.zip_code
        }

    
class CheckoutContact(Document):
    shipping_information = EmbeddedDocumentField(CheckoutInfoEmbedded, required=True)
    billing_information = EmbeddedDocumentField(CheckoutInfoEmbedded, required=True)

    def to_json(self):
        return {
            "shipping_information": self.shipping_information.to_json(),
            "billing_information": self.billing_information.to_json(),
        }


class CheckoutContactEmbedded(EmbeddedDocument):
    shipping_information = EmbeddedDocumentField(CheckoutInfoEmbedded, required=True)
    billing_information = EmbeddedDocumentField(CheckoutInfoEmbedded, required=True)
    

class ShippingState(Document):
    state = StringField(required=True, max_length=20, unique=True)
    value = DecimalField(precision=2)


class PayPal(EmbeddedDocument):
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

    # def to_json(self):
    #     return {
    #         "order_id": self.order_id,
    #         "status": self.status,
    #         "value": self.value,
    #         "name": self.name,
    #         "surname": self.surname,
    #         "full_name": self.full_name,
    #         "payer_id": self.payer_id,
    #         "email": self.email,
    #         "address": self.address,
    #         "capture_id": self.capture_id,
    #         "capture_status": self.capture_status,
    #         "purchase_breakdown": self.purchase_breakdown,
    #         "capture_time": self.capture_time,
    #         "create_time": self.create_time,
    #         "update_time": self.update_time
    #     }


class Square(EmbeddedDocument):
    created_at = DateTimeField()
    status = StringField()
    buyer_email_address = StringField()
    total_money = DecimalField(precision=2)

    # PAYMENT FIELDS
    payment_id = StringField()
    
    # SUBSCRIPTION FIELDS
    subscription_id = StringField()
    start_date = DateTimeField()


class SquarePayment(EmbeddedDocument): # https://developer.squareup.com/reference/square/objects/Payment
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
    card_error = ListField() # Information about errors encountered during the request, return an array of dicts
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
    delayed_until = DateTimeField(precision=2) # when the delay_action is automatically applied
    order_id = StringField()
    location_id = StringField()
    receipt_number = StringField() # The payment's receipt number. The field is missing if a payment is canceled.
    risk_evaluation = DictField() # Provides information about the risk associated with the payment, as determined by Square.
    buyer_email_address = StringField()
    billing_address = DictField()
    shipping_address = DictField()
    note = StringField() # An optional note to include when creating a payment.
    version_token = StringField() # Used for optimistic concurrency. This opaque token identifies a specific version of the Payment object.
    create_payment_at = DateTimeField(default=datetime.utcnow)

    # if any amount field is -100 it is because the Square Server didn't return that value
    # if any datetime field is 2000-01-01T00:00:00.000Z it is because the Square Server didn't return that value

    def to_json(self):
        return {
            "payment_id": self.payment_id,
            "status": self.status,
            "source_type": self.source_type,
            "amount_money": self.amount_money,
            "tip_money": self.tip_money,
            "approved_money": self.approved_money,
            "total_money": self.total_money,
            "fee_money": self.fee_money,
            "avs_status": self.avs_status,
            "card": self.card,
            "card_status": self.card_status,
            "card_error": self.card_error,
            "created_at": self.created_at,
            "authorized_at": self.authorized_at,
            "captured_at": self.captured_at,
            "voided_at": self.voided_at,
            "updated_at": self.updated_at,
            "cvv_status": self.cvv_status,
            "entry_method": self.entry_method,
            "statement_description": self.statement_description,
            "verification_method": self.verification_method,
            "verification_results": self.verification_results,
            "delay_action": self.delay_action,
            "delay_duration": self.delay_duration,
            "delayed_until": self.delayed_until,
            "order_id": self.order_id,
            "location_id": self.location_id,
            "receipt_number": self.receipt_number,
            "risk_evaluation": self.risk_evaluation,
            "buyer_email_address": self.buyer_email_address,
            "billing_address": self.billing_address,
            "shipping_address": self.shipping_address,
            "note": self.note,
            "version_token": self.version_token,
            "create_payment_at": self.create_payment_at
        }


class SquarePaymentError(Document): # https://developer.squareup.com/reference/square/objects/Error
    category = StringField() # The high-level category for the error | API_ERROR, AUTHENTICATION_ERROR, INVALID_REQUEST_ERROR, RATE_LIMIT_ERROR, PAYMENT_METHOD_ERROR or REFUND_ERROR
    code = StringField() # The specific code of the error. | ... see above url
    detail = StringField() # A human-readable description of the error for debugging purposes.
    field = StringField() # The name of the field provided in the original request (if any) that the error pertains to.
    customer_id = StringField()
    card_id = StringField()
    amount = DecimalField(precision=2)
    type = StringField() # The type of transaction
    created_at = DateTimeField(default=datetime.utcnow)


class Subscription(Document):
    id = StringField(primary_key=True)
    card_id = StringField()
    charged_through_date = DateTimeField()
    created_at = StringField()
    customer_id = StringField()
    location_id = StringField()
    plan_id = StringField()
    start_date = StringField()
    status = StringField()
    tax_percent = StringField()
    version = IntField()
    updated_at = DateTimeField(default=datetime.utcnow)


class Order(Document):
    type = StringField(default='ONCE')
    cart = EmbeddedDocumentListField(Cart, required=True)
    square = EmbeddedDocumentField(Square)
    paypal = EmbeddedDocumentField(PayPal)
    checkout_info = EmbeddedDocumentField(CheckoutContactEmbedded, required=True)
    shipping = DecimalField(precision=2)
    discount = DecimalField(precision=2)
    created_at = DateTimeField(default=datetime.utcnow)
