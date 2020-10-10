import graphene
from graphene_django import DjangoObjectType
from graphene_django.rest_framework.mutation import SerializerMutation
from .models import Activity, StrengthSections, Exercise, ExerciseSet, CardioSession
from users.schema import UserType
from django.core.exceptions import ValidationError
from .serializers import ActivitySerializer, SectionSerializer

class ExerciseSetInput(graphene.InputObjectType):
    weights = graphene.Int()
    reps = graphene.Int()
    notes = graphene.String()

class ExercisesInput(graphene.InputObjectType):
    exercise_name = graphene.String()
    sets = graphene.List(ExerciseSetInput)


class StrengthSectionsInput(graphene.InputObjectType):
    section_name = graphene.String()
    exercises = graphene.List(ExercisesInput)

class StrengthSectionsType(DjangoObjectType):
    class Meta:
        model = StrengthSections
class ExerciseSetType(DjangoObjectType):
    class Meta:
        model = ExerciseSet
class ExerciseType(DjangoObjectType):
    class Meta:
        model = Exercise
class Sets(graphene.ObjectType):
    notes = graphene.String()
    weights = graphene.Int()
    reps = graphene.Int()
class ExerciseObject(graphene.ObjectType):
    exercise_name = graphene.String()
    sets = graphene.List(Sets, required=False,)
class Section(graphene.ObjectType):
    section_name = graphene.String()
    exercises = graphene.List(ExerciseObject, default_value=[], required=False,)

class CardioSessionInput(graphene.InputObjectType):
    duration = graphene.Int()
    cardio_type = graphene.String()
    start_date = graphene.Date()
    end_date = graphene.Date()

class CardioSessionType(DjangoObjectType):
    class Meta:
        model = CardioSession
class ActivityType(DjangoObjectType):
    class Meta:
        model = Activity

class Query(graphene.ObjectType):
    activities = graphene.List(ActivityType)

    def resolve_activities(self, info, **kwargs):
        user = info.context.user or None
        if user.is_anonymous:
            raise Exception('You must login to see activities!')
        return Activity.objects.all()

class CreateActivity(graphene.Mutation):
    id = graphene.Int()
    activity_type = graphene.String()
    start_date = graphene.Date()
    description = graphene.String()
    name = graphene.String()
    posted_by = graphene.Field(UserType)
    cardio = graphene.Field(CardioSessionType, required=False,)
    sections = graphene.List(Section, required=False,)

    class Arguments:
        activity_type = graphene.String()
        start_date = graphene.Date()
        name = graphene.String()
        description = graphene.String()
        cardio = graphene.Argument(CardioSessionInput, required=False)
        sections = graphene.List(StrengthSectionsInput)

    def mutate(self, info, activity_type, start_date, name, description, sections, cardio=None):
        user = info.context.user or None

        # crate basic activity
        activity = Activity(
            activity_type=activity_type,
            start_date=start_date,
            name=name,
            description=description,
            posted_by=user,
            cardio=cardio
        )
        activity.save()

        # sections
        for section in sections:
            section_data = StrengthSections(
                section_name=section.section_name,
                activity = activity
            )
            section_data.save()
            # exercises
            for exercise in section.exercises:
                exercise_data = Exercise(
                    exercise_name=exercise.exercise_name,
                    section = section_data
                )
                exercise_data.save()
                # sets
                for exercise_set in exercise.sets:
                    set_data = ExerciseSet(
                        exercise=exercise_data,
                        weights=exercise_set.weights,
                        reps=exercise_set.reps,
                        notes=exercise_set.notes
                    )
                    set_data.save()
        # end section loop
        activity.save()

        activity_serializer = ActivitySerializer(instance=activity)
        sections_info = activity_serializer.data.get('sections')

        # validate
        try:
            activity.full_clean()
        except ValidationError as e:
            raise Exception(e)
            pass

        return CreateActivity(
            activity_type=activity.activity_type,
            start_date=activity.start_date,
            name=activity.name,
            description=activity.description,
            posted_by=activity.posted_by,
            cardio=activity.cardio,
            sections=sections_info
        )

class Mutation(graphene.ObjectType):
    create_activity = CreateActivity.Field()

schema = graphene.Schema(mutation=Mutation, query=Query)