from graphene import ObjectType, Mutation
from graphene import String, Boolean

from ...services.settings_service import login, update_discounts, update_password
from ...middleware import authentication_required


class Login(Mutation):
    class Arguments:
        password = String(required=True)
    
    token = String()
    success = Boolean()

    def mutate(self, info, password):
        token, success = login(password)
        print('Token:', token, success)
        return {'token': token, 'success': success}


class UpdateDiscounts(Mutation):
    class Arguments:
        month = String(required=True)
        two_months = String(required=True)

    month = String()
    two_months = String()

    @authentication_required()
    def mutate(root, info, month=None, two_months=None):
        return update_discounts(month, two_months)


class UpdatePassword(Mutation):
    class Arguments:
        password = String(required=True)
        new_password = String(required=True)

    response = String()

    @authentication_required()
    def mutate(root, info, password=None, new_password=None):
        response = update_password(password, new_password)
        return { 'response': response }


class Mutation(ObjectType):
    login = Login.Field()
    update_discounts = UpdateDiscounts.Field()
    update_password = UpdatePassword.Field()
