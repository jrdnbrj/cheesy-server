from graphene import ObjectType, Mutation, List, String, Boolean

from ..type import HomeInputType, HomeType, OurFamilyInputType, OurFamilyType
from ...services.cheesy_service import update_home, update_family, update_terms
from ...middleware import authentication_required


class UpdateHome(Mutation):
    class Arguments:
        data = List(HomeInputType, required=True)

    response = List(HomeType)

    @authentication_required()
    def mutate(root, info, data=[]):
        print('datadata:', data)
        return update_home(data)


class UpdateFamily(Mutation):
    class Arguments:
        data = List(OurFamilyInputType, required=True)

    response = List(OurFamilyType)

    @authentication_required()
    def mutate(root, info, data=[]):
        return update_family(data)


class UpdateTerms(Mutation):
    class Arguments:
        data = String()

    response = Boolean()

    @authentication_required()
    def mutate(root, info, data=''):
        return update_terms(data)


class Mutation(ObjectType):
    update_home = UpdateHome.Field()
    update_family = UpdateFamily.Field()
    update_terms = UpdateTerms.Field()
