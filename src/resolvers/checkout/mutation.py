from graphene import ObjectType, Mutation
from graphene import String, List, Boolean

from ...middleware import authentication_required
from ..type import CheckoutInfoInputType
from ...services.checkout_service import (
    create_checkout_contact, 
    create_coupon, 
    delete_coupon,
    activate_coupon,
    deactivate_coupon,
    update_shipping_values
)


class CreateCheckoutInfo(Mutation):
    class Arguments:
        shipping_info = CheckoutInfoInputType()
        billing_info = CheckoutInfoInputType()

    response = Boolean()
    id = String()

    def mutate(root, info, shipping_info, billing_info):
        contact = create_checkout_contact(shipping=shipping_info, billing=billing_info)
        return {'response': True, 'id': contact.id}


class CreateCoupon(Mutation):
    class Arguments:
        code = String(required=True)
        discount = String(required=True)
    
    response = String()

    @authentication_required()
    def mutate(root, info, code=None, discount=None):
        response = create_coupon(code=code, discount=discount)
        return {'response': response}


class DeleteCoupon(Mutation):
    class Arguments:
        code = String(required=True)
    
    response = String()

    @authentication_required()
    def mutate(root, info, code=None):
        response = delete_coupon(code)
        return {'response': response}


class ActivateCoupon(Mutation):
    class Arguments:
        code = String(required=True)
    
    response = String()

    @authentication_required()
    def mutate(root, info, code=None):
        response = activate_coupon(code)
        return {'response': response}


class DeactivateCoupon(Mutation):
    class Arguments:
        code = String(required=True)
    
    response = String()

    @authentication_required()
    def mutate(root, info, code=None):
        response = deactivate_coupon(code)
        return {'response': response}


class UpdateShippingStates(Mutation):
    class Arguments:
        values = List(String, required=True)
    
    response = Boolean()

    @authentication_required()
    def mutate(root, info, values):
        response = update_shipping_values(values)
        return {'response': response}



class Mutation(ObjectType):
    create_checkout_contact = CreateCheckoutInfo.Field()
    create_coupon = CreateCoupon.Field()
    delete_coupon = DeleteCoupon.Field()
    activate_coupon = ActivateCoupon.Field()
    deactivate_coupon = DeactivateCoupon.Field()
    update_shipping = UpdateShippingStates.Field()
