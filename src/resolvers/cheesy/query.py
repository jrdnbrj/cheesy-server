from graphene import ObjectType
from graphene import List, Int, String

from ..type import HomeType, OurFamilyType, InstagramMediaType

from ...services.cheesy_service import get_home, get_family, get_instagram_media


class Query(ObjectType):
    get_home = List(HomeType)
    get_family = List(OurFamilyType)
    get_instagram_media = List(InstagramMediaType, count=Int(required=True))

    def resolve_get_home(parent, info):
        return get_home()
    
    def resolve_get_family(parent, info):
        return get_family()

    def resolve_get_instagram_media(parent, info, count):
        return get_instagram_media(count)
