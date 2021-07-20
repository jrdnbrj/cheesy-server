from graphene import ObjectType
from graphene import List

from ..type import CheckoutContact

# from ...services.contact_service import get_contacts


class Query(ObjectType):
    get_coupons = List(CheckoutContact)

    def resolve_get_coupons(parent, info):
        return {}
