from graphene import ObjectType, Mutation
from graphene import String, Boolean

from ...services.settings_service import update_discounts, update_password


class UpdateDiscounts(Mutation):
    class Arguments:
        month = String(required=True)
        two_months = String(required=True)

    month = String()
    two_months = String()

    def mutate(root, info, month=None, two_months=None):
        return update_discounts(month, two_months)


class UpdatePassword(Mutation):
    class Arguments:
        password = String(required=True)
        new_password = String(required=True)

    response = Boolean()

    def mutate(root, info, password=None, new_password=None):
        result = update_password(password, new_password)
        return { 'result': result }


class Mutation(ObjectType):
    update_discounts = UpdateDiscounts.Field()
    update_password = UpdatePassword.Field()
