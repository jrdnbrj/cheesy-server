from graphene import ObjectType, Mutation
from graphene import String, Decimal

from ...services.product_service import create_product


class CreateProduct(Mutation):
    class Arguments:
        name = String()
        description = String()
        short_description = String()
        ingredients = String()
        price = Decimal()

    name = String()
    description = String()
    short_description = String()
    ingredients = String()
    price = String()

    def mutate(root, info, name=None, description=None, short_description=None, ingredients=None, price=None,):
        return create_product(
            name=name, 
            description=description, 
            short_description=short_description, 
            ingredients=ingredients, 
            price=price, 
        )


class Mutation(ObjectType):
    create_product = CreateProduct.Field()
