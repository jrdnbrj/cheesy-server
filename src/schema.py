from graphene import ObjectType, Schema

# queries
from .resolvers.product.query import Query as product_query
from .resolvers.paypal.query import Query as paypal_query
from .resolvers.square.query import Query as square_query
from .resolvers.contact.query import Query as contact_query
from .resolvers.checkout.query import Query as checkout_query

# mutations
from .resolvers.product.mutation import Mutation as product_mutation
from .resolvers.contact.mutation import Mutation as contact_mutation
from .resolvers.checkout.mutation import Mutation as checkout_mutation


class Query(product_query, paypal_query, square_query, contact_query, checkout_query, ObjectType): 
    pass

class Mutation(product_mutation, contact_mutation, checkout_mutation, ObjectType): 
    pass


schema = Schema(query=Query, mutation=Mutation)
