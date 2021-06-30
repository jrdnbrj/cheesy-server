from graphene import ObjectType, Mutation
from graphene import String, Decimal

from ...services.contact_service import create_contact


class CreateContact(Mutation):
    class Arguments:
        full_name = String()
        email = String()
        phone = String()
        message = String()

    full_name = String()
    email = String()
    phone = String()
    message = String()

    def mutate(root, info, full_name=None, email=None, phone=None, message=None):
        return create_contact(full_name=full_name, email=email, phone=phone, message=message)


class Mutation(ObjectType):
    create_contact = CreateContact.Field()
