from django.conf import settings
from django.db import models


class TrainingSplit(models.Model):
    name = models.TextField(default="text", blank=True)
    description = models.TextField(blank=True)
    split_length = models.IntegerField(default=7, blank=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, related_name='training_splits')


class Training(models.Model):
    start_date = models.DateField()
    name = models.TextField(default="text", blank=True)
    day_in_split = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    training_split = models.ForeignKey(TrainingSplit, related_name="trainings", null=True, blank=True, on_delete=models.CASCADE)


class Exercise(models.Model):
    STRENGTH = "STRENGTH"
    CARDIO = "CARDIO"
    TYPE_CHOICES = [
        (STRENGTH, STRENGTH),
        (CARDIO, CARDIO)
    ]
    exercise_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default=STRENGTH)
    exercise_name = models.CharField(max_length=100)
    body_part = models.CharField(max_length=100, null=True, blank=True)
    training = models.ForeignKey(Training, related_name="exercises", null=True, blank=True, on_delete=models.CASCADE)


class ExerciseSet(models.Model):
    weights = models.IntegerField(null=True, blank=True)
    reps = models.IntegerField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    distance = models.IntegerField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    exercise = models.ForeignKey(Exercise, related_name="exercise_sets", null=True, blank=True, on_delete=models.CASCADE)
