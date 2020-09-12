import graphene
from graphene_django import DjangoObjectType
from .models import Activity, StrengthSection, Exercise, ExerciseSet
from users.schema import UserType

class ExerciseSetInput(graphene.InputObjectType):
    weights = graphene.Int()
    reps = graphene.Int()
    notes = graphene.String()

class ExerciseSetType(DjangoObjectType):
    class Meta:
        model = ExerciseSet
class ExerciseInput(graphene.InputObjectType):
    exercise_name = graphene.String()
    sets = graphene.List(ExerciseSetInput)

class ExerciseType(DjangoObjectType):
    class Meta:
        model = Exercise
class StrengthSectionInput(graphene.InputObjectType):
    name = graphene.String()
    section_name = graphene.String()
    exercises = ExerciseInput()

class StrengthSectionType(DjangoObjectType):
    class Meta:
        model = StrengthSection
class ActivityType(DjangoObjectType):
    class Meta:
        model = Activity

class Query(graphene.ObjectType):
    activities = graphene.List(ActivityType)

    def resolve_activities(self, info, **kwargs):
        return Activity.objects.all()

class CreateActivity(graphene.Mutation):
    id = graphene.Int()
    activity_type = graphene.String()
    start_date = graphene.Date()
    description = graphene.String()
    posted_by = graphene.Field(UserType)
    strength = graphene.Field(StrengthSectionType)

    class Arguments:
        activity_type = graphene.String()
        start_date = graphene.Date()
        description = graphene.String()
        strength = StrengthSectionInput()

    def mutate(self, info, activity_type, start_date, description, strength):
        user = info.context.user or None

        sets = []
        for set in strength.exercises.sets:
            print(set)
            set_data = ExerciseSet(
                id=100,
                weights=set.weights,
                reps=set.reps,
                notes=set.notes
            )
            set_data.save()
            sets.append(set_data)
            
        exercises = Exercise(
            exercise_name = strength.exercises.exercise_name,
        )

        exercises.save()

        exercises.sets.set(sets)

        exercises.save()

        strength_field = StrengthSection(
            name=strength.name,
            section_name=strength.section_name,
            exercises=exercises
        )
        strength_field.save()
        
        activity = Activity(
            activity_type=activity_type,
            start_date=start_date,
            description=description,
            posted_by=user,
            strength=strength_field,
        )
        activity.save()

        return CreateActivity(
            activity_type=activity.activity_type,
            start_date=activity.start_date,
            description=activity.description,
            posted_by=activity.posted_by,
            strength=activity.strength,
        )

class Mutation(graphene.ObjectType):
    create_activity = CreateActivity.Field()

schema = graphene.Schema(mutation=Mutation, query=Query)