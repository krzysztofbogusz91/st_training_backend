import graphene
from graphene_django import DjangoObjectType
from .models import Activity
from users.schema import UserType
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

    class Arguments:
        activity_type = graphene.String()
        start_date = graphene.Date()
        description = graphene.String()

    def mutate(self, info, activity_type, start_date, description):
        user = info.context.user or None
        activity = Activity(
            activity_type=activity_type,
            start_date=start_date,
            description=description,
            posted_by=user,
        )
        activity.save()

        return CreateActivity(
            activity_type=activity.activity_type,
            start_date=activity.start_date,
            description=activity.description,
            posted_by=activity.posted_by,
        )

class Mutation(graphene.ObjectType):
    create_activity = CreateActivity.Field()

schema = graphene.Schema(mutation=Mutation, query=Query)