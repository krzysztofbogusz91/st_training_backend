import graphene
from graphql_jwt.decorators import login_required

from ..models import (
    TrainingSplit,
    Training,
    Exercise,
    ExerciseSet
)
from .types import (
    TrainingSplitType,
    TrainingType,
    ExerciseType,
    ExerciseSetType,
)


class ExerciseSetInput(graphene.InputObjectType):
    weights = graphene.Int()
    reps = graphene.Int()
    duration = graphene.Int()
    distance = graphene.Int()
    notes = graphene.String()


class ExerciseInput(graphene.InputObjectType):
    exercise_type = graphene.String()
    exercise_name = graphene.String()
    body_part = graphene.String()
    exercise_sets = graphene.List(ExerciseSetInput)


class TrainingInput(graphene.InputObjectType):
    start_date = graphene.Date()
    name = graphene.String()
    day_in_split = graphene.Int()
    description = graphene.String()
    exercises = graphene.List(ExerciseInput)


class TrainingSplitInput(graphene.InputObjectType):
    name = graphene.String()
    description = graphene.String()
    split_length = graphene.Int()
    trainings = graphene.List(TrainingInput)


class CreateTrainingSplitMutation(graphene.Mutation):
    class Arguments:
        training_split = TrainingSplitInput(required=True)

    # Output
    training_split = graphene.Field(TrainingSplitType)

    @login_required
    def mutate(self, info, **kwargs):
        user = info.context.user

        training_split_input = kwargs.get('training_split')
        training_split = TrainingSplit.objects.create(
            posted_by=user,
            name=training_split_input.get('name'),
            description=training_split_input.get('description'),
            split_length=training_split_input.get('split_length'),
        )

        trainings_input = training_split_input.get('trainings')
        if trainings_input:
            for training_input in trainings_input:
                training = Training.objects.create(
                    name=training_input.get('name'),
                    description=training_input.get('description'),
                    start_date=training_input.get('start_date'),
                    day_in_split=training_input.get('day_in_split'),
                    training_split=training_split
                )

                exercises_input = training_input.get('exercises')
                if exercises_input:
                    for exercise_input in exercises_input:
                        exercise = Exercise.objects.create(
                            exercise_name=exercise_input.get('exercise_name'),
                            exercise_type=exercise_input.get('exercise_type'),
                            body_part=exercise_input.get('body_part'),
                            training=training
                        )

                        exercise_sets_input = exercise_input.get('exercise_sets')
                        if exercise_sets_input:
                            for exercise_set_input in exercise_sets_input:
                                exercise_set = ExerciseSet.objects.create(
                                    weights=exercise_set_input.get('weights'),
                                    reps=exercise_set_input.get('reps'),
                                    duration=exercise_set_input.get('duration'),
                                    distance=exercise_set_input.get('distance'),
                                    notes=exercise_set_input.get('notes'),
                                    exercise=exercise
                                )

        return CreateTrainingSplitMutation(training_split=training_split)
