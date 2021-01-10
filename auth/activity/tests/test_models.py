from activity.models import Activity, StrengthSections, Exercise, ExerciseSet
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from django.core.exceptions import ValidationError

# Create your tests here.
class ActivityModelTests(TestCase):
    def setUp(self):
      self.user1 = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')

    def test_can_crate_basic_activity_with_no_sections(self):
        """
        tests if activity can be crated with no additional data
        """
        start_date = time = timezone.now()
        activity_type = Activity.STRENGTH
        name = 'Test Training'
        new_activity = Activity(
          start_date=start_date,
          activity_type=activity_type,
          name = name,
          posted_by=self.user1,
        )
        new_activity.save()
        self.assertEqual(new_activity.name, name)

    def test_can_crate_activity_with_section(self):
        """
        tests if activity section is connected to activity correctly
        """
        start_date = time = timezone.now()
        activity_type = Activity.STRENGTH
        name = 'Test Training'
        new_activity = Activity(
          start_date=start_date,
          activity_type=activity_type,
          name = name,
          posted_by=self.user1,
        )
        new_activity.save()

        section_data = StrengthSections(
          section_name='MAIN',
          activity = new_activity
        )

        section_data.save()
        
        self.assertEqual(new_activity.get_sections().count(), 1)
  
    def test_can_crate_activity_with_complete_set_of_data(self):
        """
        tests if activity can have sections containing exercises and sets 
        """
        start_date = time = timezone.now()
        activity_type = Activity.STRENGTH
        name = 'Test Training'
        new_activity = Activity(
          start_date=start_date,
          activity_type=activity_type,
          name = name,
          posted_by=self.user1,
        )
        new_activity.save()

        section_data = StrengthSections(
          section_name='MAIN',
          activity = new_activity
        )

        section_data.save()

        exercise = Exercise(
          exercise_name="PUSH UP",
          section=section_data
        )

        exercise.save()

        ex_set = ExerciseSet(
          exercise=exercise,
          weights=10,
          reps=10,
          notes='Notes'
        )
        ex_set.save()

        self.assertEqual(new_activity.get_sections().count(), 1)
        self.assertEqual(section_data.get_exercises().count(), 1)
        self.assertEqual(exercise.get_sets().count(), 1)
        self.assertEqual(ex_set.exercise.pk, exercise.pk)
        

    def test_activity_can_only_accept_correct_type_throws_err_with_wrong(self):
        """
        tests if activity section is connected to activity correctly
        """
        start_date = time = timezone.now()
        activity_type = 'WRONG TYPE'
        name = 'Test Training'
        new_activity = Activity(
          start_date=start_date,
          activity_type=activity_type,
          name = name,
          posted_by=self.user1,
        )

        new_activity.save()

        with self.assertRaises(ValidationError):
            new_activity.full_clean()

    def test_activity_can_only_accept_correct_type(self):
        """
        tests if activity section is connected to activity correctly
        """
        start_date = time = timezone.now()
        activity_type = Activity.STRENGTH
        name = 'Test Training'
        new_activity = Activity(
          start_date=start_date,
          activity_type=activity_type,
          name = name,
          posted_by=self.user1,
        )
        
        new_activity.save()
        new_activity.full_clean()
        
        self.assertEqual(new_activity.activity_type, Activity.STRENGTH)