from graphene import ObjectType, Mutation
from graphene import String, Decimal, List, Boolean

from ...services.product_service import edit_product
from ...middleware import authentication_required


class EditProduct(Mutation):
    class Arguments:
        name = String(required=True)
        images = List(String, required=True)
        price = Decimal(required=True)
        description = String(required=True)
        short_description = String(required=True)
        ingredients = List(String, required=True)
        path = String(required=True)
        smoothies = List(List(String), required=True)

    result = Boolean()

    @authentication_required()
    def mutate(root, info, name=None, images=None, price=None, description=None, short_description=None, ingredients=None, path=None, smoothies=None):
        print('Actualizando Producto...')
        result = edit_product(
            name=name, 
            images=images, 
            price=price, 
            description=description, 
            short_description=short_description, 
            ingredients=ingredients, 
            path=path, 
            smoothies=smoothies
        )
        return { 'result': result }


class Mutation(ObjectType):
    edit_product = EditProduct.Field()
