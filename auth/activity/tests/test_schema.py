import json

from activity.models import Activity, StrengthSections
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from graphene_django.utils.testing import GraphQLTestCase
from graphql_jwt.shortcuts import get_token


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
        
        token = get_token(get_user_model().objects.get(pk=self.user1.pk))
        headers = {"Authorization": f"JWT {token}"}
        response = self.query(
            '''
              query {
                activities {
                  id
                  activityType,
                  startDate,
                  name,
                  description,
                  postedBy {
                    username
                  },
                  cardio {
                    duration,
                    startDate,
                    endDate,
                    cardioType
                  },
                  sections {
                    id
                    sectionName,
                    exercises {
                      id
                      exerciseName
                      sets {
                        id
                        weights,
                        reps,
                        notes
                      }
                    }
                  }
                }
              }
            ''',
            headers=headers,
        )

        content = json.loads(response.content)
        activiesResponse = content['data']['activities']

        self.assertResponseNoErrors(response)
        self.assertEqual(len(activiesResponse), 1)

    def test_user_log_in(self):
        """
         Test user can login and will get token
        """
        
        response = self.query(
            '''
              mutation {
                tokenAuth(username: "jacob", password: "top_secret") {
                token
                  payload
                  refreshExpiresIn
                  refreshToken
                }
              }
            ''',
        )

        content = json.loads(response.content)
        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)
        self.assertTrue(content['data'])