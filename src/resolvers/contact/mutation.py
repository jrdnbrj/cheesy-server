from graphene import ObjectType, Mutation
from graphene import String, Boolean

from ...services.contact_service import create_contact, delete_contact


class CreateContact(Mutation):
    class Arguments:
        full_name = String()
        email = String()
        phone = String()
        message = String()

    id = String()
    full_name = String()
    email = String()
    phone = String()
    message = String()

    def mutate(root, info, full_name=None, email=None, phone=None, message=None):
        return create_contact(full_name=full_name, email=email, phone=phone, message=message)


class DeleteContact(Mutation):
    class Arguments:
        id = String(required=True)

    result = Boolean()

    def mutate(root, info, id=None):
        result = delete_contact(id)
        return { 'result': result }


class Mutation(ObjectType):
    create_contact = CreateContact.Field()
    delete_contact = DeleteContact.Field()
