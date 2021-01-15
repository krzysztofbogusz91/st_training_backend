import graphene

from .queries import (
    TrainingSplitQuery
)
from .mutations import (
    CreateTrainingSplitMutation
)


class Query(
    TrainingSplitQuery,
    graphene.ObjectType
):
    pass


class Mutation(graphene.ObjectType):
    create_training_split = CreateTrainingSplitMutation.Field()
