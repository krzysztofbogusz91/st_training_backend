import graphene
from graphene_django import DjangoObjectType
from .models import Activity, StrengthSections, Exercise, ExerciseSet
from users.schema import UserType
from django.core.exceptions import ValidationError

class ExerciseSetInput(graphene.InputObjectType):
    weights = graphene.Int()
    reps = graphene.Int()
    notes = graphene.String()

class ExerciseSetType(DjangoObjectType):
    class Meta:
        model = ExerciseSet
class ExercisesInput(graphene.InputObjectType):
    exercise_name = graphene.String()
    sets = graphene.List(ExerciseSetInput)

class ExerciseType(DjangoObjectType):
    class Meta:
        model = Exercise
class StrengthSectionsInput(graphene.InputObjectType):
    section_name = graphene.String()
    exercises = graphene.List(ExercisesInput)

class StrengthSectionsType(DjangoObjectType):
    class Meta:
        model = StrengthSections
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
    strength = graphene.List(StrengthSectionsType)

    class Arguments:
        activity_type = graphene.String()
        start_date = graphene.Date()
        name = graphene.String()
        description = graphene.String()
        strength = graphene.List(StrengthSectionsInput)

    def mutate(self, info, activity_type, start_date, name, description, strength):
        user = info.context.user or None
        
        sections = []
        exercises = []
        sets = []
        # sections
        for section in strength:
            section_data = StrengthSections(
                section_name=section.section_name
            )
            section_data.save()
            # exercises
            for exercise in section.exercises:
                exercise_data = Exercise(
                    exercise_name=exercise.exercise_name,
                )
                exercise_data.save()
                # sets
                for exercise_set in exercise.sets:
                    set_data = ExerciseSet(
                        weights=exercise_set.weights,
                        reps=exercise_set.reps,
                        notes=exercise_set.notes
                    )
                    set_data.save()
                    sets.append(set_data)
                # set exercise sets
                exercise_data.sets.set(sets)
                exercise_data.save()
                exercises.append(exercise_data)
            # set section exercises
            section_data.exercises.set(exercises)
            section_data.save()
            # append to main array
            sections.append(section_data)
        # end section loop
        activity = Activity(
            activity_type=activity_type,
            start_date=start_date,
            name=name,
            description=description,
            posted_by=user,
        )

        # validate
        try:
            activity.full_clean()
        except ValidationError as e:
            raise Exception(e)
            pass

        activity.save()
        activity.strength.set(sections)
        activity.save()

        return CreateActivity(
            activity_type=activity.activity_type,
            start_date=activity.start_date,
            name=activity.name,
            description=activity.description,
            posted_by=activity.posted_by,
            strength=sections,
        )

class Mutation(graphene.ObjectType):
    create_activity = CreateActivity.Field()

schema = graphene.Schema(mutation=Mutation, query=Query)