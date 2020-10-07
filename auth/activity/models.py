from django.db import models
from django.conf import settings
class ExerciseSet(models.Model):
    weights = models.IntegerField()
    reps = models.IntegerField()
    notes = models.TextField(blank=True)
class Exercise(models.Model):
    exercise_name = models.CharField(max_length=100)
    sets = models.ManyToManyField(ExerciseSet, related_name='exercise_set', null = True, blank = True,)
class StrengthSections(models.Model):
    section_name = models.CharField(max_length=100)
    exercises = models.ManyToManyField(Exercise, related_name='exercise', null = True, blank = True,)


class Activity(models.Model):
    STRENGTH = "STRENGTH"
    CARDIO = "CARDIO"
    TYPE_CHOICES = [
        (STRENGTH, STRENGTH),
        (CARDIO, CARDIO)
    ]
    activity_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default=STRENGTH)
    start_date = models.DateField()
    name = models.TextField(default="text", blank=True)
    description = models.TextField(blank=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    strength = models.ManyToManyField(StrengthSections, related_name='exercise', null = True, blank = True,)