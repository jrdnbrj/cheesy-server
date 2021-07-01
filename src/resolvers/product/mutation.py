from graphene import ObjectType, Mutation
from graphene import String, Decimal, List, Boolean

from ...services.product_service import edit_product


class EditProduct(Mutation):
    class Arguments:
        name = String(required=True)
        images = List(String, required=True)
        price = Decimal(required=True)
        description = String(required=True)
        short_description = String(required=True)
        ingredients = List(String, required=True)
        path = String(required=True)

    result = Boolean()

    def mutate(root, info, name=None, images=None, price=None, description=None, short_description=None, ingredients=None, path=None):
        result = edit_product(
            name=name, 
            images=images, 
            price=price, 
            description=description, 
            short_description=short_description, 
            ingredients=ingredients, 
            path=path, 
        )
        return { 'result': result }


class Mutation(ObjectType):
    edit_product = EditProduct.Field()
