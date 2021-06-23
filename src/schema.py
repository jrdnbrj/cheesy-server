from graphene import ObjectType, Schema

# queries
from .resolvers.product.query import Query as product_query
from .resolvers.paypal.query import Query as paypal_query
from .resolvers.square.query import Query as square_query

# mutations
from .resolvers.product.mutation import Mutation as product_mutation


class Query(product_query, paypal_query, square_query, ObjectType): pass

class Mutation(product_mutation, ObjectType): pass


schema = Schema(query=Query, mutation=Mutation)
