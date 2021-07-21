from graphene import ObjectType
from graphene import List

from ..type import CouponType

from ...services.checkout_service import get_coupons


class Query(ObjectType):
    get_coupons = List(CouponType)

    def resolve_get_coupons(parent, info):
        return get_coupons()
