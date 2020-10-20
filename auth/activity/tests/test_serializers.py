from activity.models import Activity, StrengthSections
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone


# Create your tests here.
class ActivityModelTests(TestCase):
    def setUp(self):
      self.user1 = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')

   