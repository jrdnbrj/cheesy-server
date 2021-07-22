from graphene import ObjectType, Mutation
from graphene import List

from ..type import HomeInputType, HomeType, OurFamilyInputType, OurFamilyType
from ...services.cheesy_service import update_home, update_family
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


class Mutation(ObjectType):
    update_home = UpdateHome.Field()
    update_family = UpdateFamily.Field()
