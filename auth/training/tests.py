import json
from graphene_django.utils.testing import GraphQLTestCase
from graphql_jwt.shortcuts import get_token
from django.contrib.auth import get_user_model


class MutationTestCase(GraphQLTestCase):
    GRAPHQL_URL = '/graphql'

    def setUp(self):
        self.user = get_user_model().objects.create(
            username='user123',
            email='user123@email.com',
            password='pass123'
        )

    def test_token_not_provided(self):
        resp = self.query(
            """
            mutation {
                createTrainingSplit(
                    trainingSplit: {}
                ) {
                    trainingSplit {
                        name
                        description
                    }
                }
            }
            """
        )

        content = json.loads(resp.content)

        self.assertEqual(resp.status_code, 200)
        self.assertResponseHasErrors(resp)
        self.assertEqual(content['errors'][0]['message'], 'You do not have permission to perform this action')

    def test_token_expired(self):
        resp = self.query(
            """
            mutation {
                createTrainingSplit(
                    trainingSplit: {}
                ) {
                    trainingSplit {
                        name
                        description
                    }
                }
            }
            """,
            headers={
                'Authorization': 'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFiZGVsbGF0aWYiLCJleHAiOjE2MTA2NDEzMzIsIm9yaWdJYXQiOjE2MTA2MzUzMzJ9.GFHlMEyZ47PWkWDy-ji-ghV89aEorh8kq7iMsNHZsHg'
            }
        )

        content = json.loads(resp.content)

        self.assertEqual(resp.status_code, 200)
        self.assertResponseHasErrors(resp)
        self.assertEqual(content['errors'][0]['message'], 'You do not have permission to perform this action')

    def test_token_valid(self):
        token = get_token(self.user)
        resp = self.query(
            """
            mutation {
                createTrainingSplit(
                    trainingSplit: {
                        name: "training split name",
                        description: "training split description",
                        splitLength: 8
                    }
                ) {
                    trainingSplit {
                        name
                        description
                    }
                }
            }
            """,
            headers={
                'HTTP_AUTHORIZATION': f'JWT {token}'
            }
        )

        self.assertEqual(resp.status_code, 200)
        self.assertResponseNoErrors(resp)
