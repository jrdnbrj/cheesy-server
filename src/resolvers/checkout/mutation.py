from graphene import ObjectType, Mutation
from graphene import String

from ..type import CheckoutInfoInputType

from ...services.checkout_service import create_checkout_contact


class CreateCheckoutInfo(Mutation):
    class Arguments:
        shipping_info = CheckoutInfoInputType()
        billing_info = CheckoutInfoInputType()

    response = String()

    def mutate(root, info, shipping_info, billing_info):
        print('Shipping Info:', shipping_info)
        print('Billing Info:', billing_info)
        create_checkout_contact(shipping=shipping_info, billing=billing_info)
        return {'response': 'success'}


class Mutation(ObjectType):
    create_checkout_contact = CreateCheckoutInfo.Field()
