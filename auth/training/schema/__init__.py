import graphene

from .queries import (
    TrainingSplitQuery
)


class Query(
    TrainingSplitQuery,
    graphene.ObjectType
):
    pass


class Mutation(graphene.ObjectType):
    pass
