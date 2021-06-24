from graphene import ObjectType
from graphene import String, Field, JSONString

from ...services.square_service import create_payment


class Query(ObjectType):
    create_payment = Field(String, payment_token=String(required=True))

    def resolve_create_payment(parent, info, payment_token):
        payment = create_payment(payment_token, 0.4)
        # print('Payment:', payment)
        return 'Hola'
    