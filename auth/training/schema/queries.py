import graphene
from graphql_jwt.decorators import login_required

from ..models import (
    TrainingSplit
)
from .types import (
    TrainingSplitType,
    TrainingType,
    ExerciseType,
    ExerciseSetType
)


class TrainingSplitQuery(graphene.ObjectType):
    training_split = graphene.List(TrainingSplitType, id=graphene.ID(required=True))
    training_splits = graphene.List(TrainingSplitType)
    my_training_splits = graphene.List(TrainingSplitType)

    @login_required
    def resolve_training_split(self, info, **kwargs):
        id = kwargs.get('id')
        return TrainingSplit.objects.get(pk=id)

    @login_required
    def resolve_training_splits(self, info, **kwargs):
        return TrainingSplit.objects.all()

    @login_required
    def resolve_my_training_splits(self, info, **kwargs):
        user = info.context.user
        return TrainingSplit.objects.filter(posted_by=user)
