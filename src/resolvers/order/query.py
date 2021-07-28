from graphene import ObjectType
from graphene import List

from ...services.order_service import get_orders
from ...middleware import authentication_required
from ..type import OrderType


class Query(ObjectType):
    get_orders = List(OrderType)

    @authentication_required()
    def resolve_get_orders(parent, info):
        return get_orders()
