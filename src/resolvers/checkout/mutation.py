from graphene import ObjectType, Mutation
from graphene import String, Boolean

from ..type import CheckoutInfoInputType

from ...services.checkout_service import (
    create_checkout_contact, 
    create_coupon, 
    delete_coupon,
    activate_coupon,
    deactivate_coupon
)


class CreateCheckoutInfo(Mutation):
    class Arguments:
        shipping_info = CheckoutInfoInputType()
        billing_info = CheckoutInfoInputType()

    response = String()

    def mutate(root, info, shipping_info, billing_info):
        create_checkout_contact(shipping=shipping_info, billing=billing_info)
        return {'response': 'success'}


class CreateCoupon(Mutation):
    class Arguments:
        code = String(required=True)
        discount = String(required=True)
    
    response = String()

    def mutate(root, info, code=None, discount=None):
        create_coupon(code=code, discount=discount)
        return {'response': 'success'}


class DeleteCoupon(Mutation):
    class Arguments:
        code = String(required=True)
    
    response = Boolean()

    def mutate(root, info, code=None):
        response = delete_coupon(code)
        return {'response': response}


class ActivateCoupon(Mutation):
    class Arguments:
        code = String(required=True)
    
    response = Boolean()

    def mutate(root, info, code=None):
        response = activate_coupon(code)
        return {'response': response}


class DeactivateCoupon(Mutation):
    class Arguments:
        code = String(required=True)
    
    response = Boolean()

    def mutate(root, info, code=None):
        response = deactivate_coupon(code)
        return {'response': response}


class Mutation(ObjectType):
    create_checkout_contact = CreateCheckoutInfo.Field()
    create_coupon = CreateCoupon.Field()
    delete_coupon = DeleteCoupon.Field()
    activate_coupon = ActivateCoupon.Field()
    deactivate_coupon = DeactivateCoupon.Field()
