import json

from activity.models import Activity, StrengthSections
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase
from django.utils import timezone
from graphene_django.utils.testing import GraphQLTestCase
from graphene.test import Client
from graphql import GraphQLError
from graphql_jwt.shortcuts import get_token
from activity.schema import schema
from activity.tests.test_helpers.queries import activity_query, token_auth_query

class TestContext: 
    def __init__(self, user):
        self.user = user

# Create your tests here.
class ActivitySchemaTests(GraphQLTestCase):
    @classmethod
    def setUpClass(cls):
        super(ActivitySchemaTests, cls).setUpClass()
        # sets up basic user for tests
        cls.user1 = User.objects.create_user(username='jacob', email='jacob@…', password='top_secret')
        cls.GRAPHQL_URL = '/graphql'

    def test_get_activies_as_logged_user(self):
        """
         Test get Activities query
        """

        new_activity = Activity(
          start_date=timezone.now(),
          activity_type=Activity.STRENGTH,
          name = 'name',
          posted_by=self.user1,
        )
        new_activity.save()
        
        context_value = TestContext(user=self.user1)
        client = Client(schema, context_value=context_value)

        query = activity_query

        response = client.execute(query)
        activiesResponse = response['data']['activities']
        userName = response['data']['activities'][0]['postedBy']['username']

        self.assertEqual(len(activiesResponse), 1)
        self.assertEqual(userName, 'jacob')

    def test_unauth_user_cannot_access_activities(self):
        """
         Unatenticated user test
        """

        new_activity = Activity(
          start_date=timezone.now(),
          activity_type=Activity.STRENGTH,
          name = 'name',
          posted_by=self.user1,
        )
        new_activity.save()
        
        response = self.query(activity_query)

        content = json.loads(response.content)
        self.assertResponseHasErrors(response)
        self.assertTrue(content['errors'])
        self.assertTrue(content['errors'][0]['message'] == 'You must login to see activities!')



    def test_user_log_in(self):
        """
         Test user can login and will get token
        """
        
        response = self.query(token_auth_query)

        content = json.loads(response.content)
        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)
        self.assertTrue(content['data'])