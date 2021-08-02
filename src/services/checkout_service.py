from ..db.documents import CheckoutContact, Coupon, ShippingState

from decimal import Decimal


def create_checkout_contact(shipping, billing):
    contact = CheckoutContact(shipping_information=shipping, billing_information=billing)
    contact.save()
    return contact

def get_checkout_contact(id):
    try:
        contact = CheckoutContact.objects(id=id).first()
        return contact
    except:
        return False

def get_coupons():
    return Coupon.objects()

def check_coupon(code):
    try:
        coupon = Coupon.objects(code=code, is_active=True).first()
        if coupon:
            return coupon
        else:
            return { 'code': 'The coupon "{}" does not exist.'.format(code) }
    except:
        return { 'code': 'Failed to detect coupon, please try again.'}

def create_coupon(**kwargs):
    code = kwargs['code']
    if (len(code) > 10):
        return 'The coupon code has more than 10 characters'
    coupon = Coupon.objects(code=code).first()
    if coupon:
        return 'The coupon already exists.'
    Coupon(**kwargs).save()
    return 'OK'

def delete_coupon(code):
    print('Delete Coupon:', code)
    try:
        coupon = Coupon.objects(code=code).first()
        coupon.delete()
        return 'OK'
    except:
        return 'The coupon {} does not exist.'.format(code)

def activate_coupon(code):
    print('Activate Coupon:', code)
    try:
        coupon = Coupon.objects(code=code).first()
        coupon.is_active = True
        coupon.save()
        return 'OK'
    except:
        return 'The coupon {} does not exist.'.format(code)

def deactivate_coupon(code):
    print('Deactivate Coupon:', code)
    try:
        coupon = Coupon.objects(code=code).first()
        coupon.is_active = False
        coupon.save()
        return 'OK'
    except:
        return 'The coupon {} does not exist.'.format(code)
    
def get_shippings():
    return ShippingState.objects().order_by('state')

def get_shipping_by_state(state):
    shipping = ShippingState.objects(state=state.upper()).first()
    
    if not shipping:
        return False, 'The state of shipping information is not available.'
    
    return True, shipping.value

def update_shipping_values(values):
    try:
        shippings = ShippingState.objects().order_by('state')

        for i, shipping in enumerate(shippings):
            new_shipping = round(Decimal(values[i]), 2)
            if shipping.value != new_shipping:
                shipping.value = new_shipping
                shipping.save()

        return True
    except:
        return False
