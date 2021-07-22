from graphene import ObjectType
from graphene import List

from ..type import HomeType, OurFamilyType

from ...services.cheesy_service import get_home, get_family


class Query(ObjectType):
    get_home = List(HomeType)
    get_family = List(OurFamilyType)

    def resolve_get_home(parent, info):
        return get_home()
    
    def resolve_get_family(parent, info):
        return get_family()
