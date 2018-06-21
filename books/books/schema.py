import graphene

import authors.schema
import basic_schema


class Query(authors.schema.Query, basic_schema.Query, graphene.ObjectType):
    pass


class Mutation(authors.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
