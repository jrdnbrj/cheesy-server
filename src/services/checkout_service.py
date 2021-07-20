from ..db.documents import CheckoutContact


def create_checkout_contact(shipping, billing):
    CheckoutContact(shipping_information=shipping, billing_information=billing).save()

