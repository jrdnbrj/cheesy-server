from graphene import ObjectType
from graphene import List, Field, String

from ..type import CouponType, ShippingStateType, ShippingResponseType
from ...services.checkout_service import (
    get_coupons, 
    check_coupon, 
    get_shippings,
    get_shipping_by_state
)
from ...middleware import authentication_required


class Query(ObjectType):
    get_coupons = List(CouponType)
    check_coupon = Field(CouponType, code=String(required=True))
    get_shippings = List(ShippingStateType)
    get_shipping_by_state = Field(ShippingResponseType, state=String(required=True))

    @authentication_required()
    def resolve_get_coupons(parent, info):
        return get_coupons()

    def resolve_check_coupon(parent, info, code):
        return check_coupon(code)

    def resolve_get_shippings(parent, info):
        return get_shippings()

    def resolve_get_shipping_by_state(parent, info, state):
        response, value = get_shipping_by_state(state)
        return { 'response': response, 'value': value }
