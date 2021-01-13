import graphene
from django.core.exceptions import ValidationError
from graphene_django import DjangoObjectType
from users.schema import UserType
from graphql import GraphQLError
from .models import TrainingSplit, Training

# Django Types
class TrainingSplitType(DjangoObjectType):
    class Meta:
        model = TrainingSplit

# Queries
class Query(graphene.ObjectType):
    splits = graphene.List(TrainingSplitType)

    def resolve_splits(self, info, **kwargs):
        user = info.context.user or None
        if user.is_anonymous:
            raise GraphQLError('You must login to see activities!')
        return TrainingSplit.objects.all()

schema = graphene.Schema(query=Query)

