from ..db.documents import CheckoutContact, Coupon


def create_checkout_contact(shipping, billing):
    CheckoutContact(shipping_information=shipping, billing_information=billing).save()

def get_coupons():
    return Coupon.objects()

def create_coupon(**kwargs):
    return Coupon(**kwargs).save()

def delete_coupon(code):
    try:
        coupon = Coupon.objects(code=code).first()
        coupon.delete()
        return True
    except:
        return False

def activate_coupon(code):
    try:
        coupon = Coupon.objects(code=code).first()
        coupon.is_active = True
        coupon.save()
        return True
    except:
        return False

def deactivate_coupon(code):
    try:
        coupon = Coupon.get(code=code).first()
        coupon.is_active = False
        coupon.save()
        return True
    except:
        return False
    
