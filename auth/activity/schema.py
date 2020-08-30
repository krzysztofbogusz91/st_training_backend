import graphene
from graphene_django import DjangoObjectType
from .models import Activity

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

    class Arguments:
        activity_type = graphene.String()
        start_date = graphene.Date()
        description = graphene.String()

    def mutate(self, info, activity_type, start_date, description):
        activity = Activity(activity_type=activity_type, start_date=start_date, description=description)
        activity.save()

        return CreateActivity(
            activity_type=activity.activity_type,
            start_date=activity.start_date,
            description=activity.description
        )

class Mutation(graphene.ObjectType):
    create_activity = CreateActivity.Field()

schema = graphene.Schema(mutation=Mutation, query=Query)