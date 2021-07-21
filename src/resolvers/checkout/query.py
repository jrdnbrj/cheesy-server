from graphene import ObjectType
from graphene import List, Field, String

from ..type import CouponType

from ...services.checkout_service import get_coupons, check_coupon


class Query(ObjectType):
    get_coupons = List(CouponType)
    check_coupon = Field(CouponType, code=String(required=True))

    def resolve_get_coupons(parent, info):
        return get_coupons()

    def resolve_check_coupon(parent, info, code):
        return check_coupon(code)
