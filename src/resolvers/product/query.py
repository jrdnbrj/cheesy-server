from graphene import ObjectType
from graphene import String, Int, List, Field

from ..type import ProductType

from ...services.product_service import get_products, get_product_by_path


class Query(ObjectType):
    get_products = List(ProductType)
    get_product_by_path = Field(ProductType, path=String(required=True))

    def resolve_get_products(parent, info):
        return get_products()

    def resolve_get_product_by_path(parent, info, path):
        return get_product_by_path(path)
