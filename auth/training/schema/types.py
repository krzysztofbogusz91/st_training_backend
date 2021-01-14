from graphene_django import DjangoObjectType

from ..models import (
    TrainingSplit,
    Training,
    Exercise,
    ExerciseSet,
)


class TrainingSplitType(DjangoObjectType):
    class Meta:
        model = TrainingSplit
        fields = '__all__'


class TrainingType(DjangoObjectType):
    class Meta:
        model = Training
        fields = '__all__'


class ExerciseType(DjangoObjectType):
    class Meta:
        model = Exercise
        fields = '__all__'


class ExerciseSetType(DjangoObjectType):
    class Meta:
        model = ExerciseSet
        fields = '__all__'
