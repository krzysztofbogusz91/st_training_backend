from django.db import models
from django.conf import settings
# TODO accept only precise types of activity_type
# class ExerciseSet(models.Model):
#     weights = models.IntegerField()
#     reps = models.IntegerField()
#     notes = models.TextField(blank=True)
# class Exercise(models.Model):
#     exercise_name = models.CharField(max_length=100)
#     sets = models.ForeignKey(ExerciseSet, null=True, on_delete=models.CASCADE)
class StrengthSection(models.Model):
    name = models.TextField(blank=True)
    section_name = models.CharField(max_length=100)
    # exercises = models.ForeignKey(Exercise, null=True, on_delete=models.CASCADE)
# class CardioSection(models.Model):
#     name = models.CharField(max_length=100)
#     section_name = models.CharField(max_length=100)
    # exercises = models.ForeignKey(Exercise, null=True, on_delete=models.CASCADE)
class Activity(models.Model):
    activity_type = models.CharField(max_length=30)
    start_date = models.DateField()
    description = models.TextField(blank=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    strength = models.ForeignKey('activity.StrengthSection',primary_key=True, related_name='strength', null=False,unique=True, on_delete=models.CASCADE)