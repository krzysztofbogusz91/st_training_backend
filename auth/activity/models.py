from django.conf import settings
from django.db import models

class CardioSession(models.Model):
    duration = models.IntegerField()
    cardio_type = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()

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
    cardio = models.ForeignKey(CardioSession, blank = True, null=True, on_delete=models.CASCADE)

    def get_sections(self):
        return self.sections.all()

class StrengthSections(models.Model):
    section_name = models.CharField(max_length=100)
    activity = models.ForeignKey(Activity, related_name="sections", null=True, blank = True, on_delete=models.CASCADE)

    def get_exercises(self):
        return self.exercises.all()

class Exercise(models.Model):
    exercise_name = models.CharField(max_length=100)
    section = models.ForeignKey(StrengthSections, related_name="exercises", null=True, blank = True, on_delete=models.CASCADE)
    
    def get_sets(self):
        return self.sets.all()
class ExerciseSet(models.Model):
    exercise = models.ForeignKey(Exercise, related_name="sets", null=True, blank = True, on_delete=models.CASCADE)
    weights = models.IntegerField()
    reps = models.IntegerField()
    notes = models.TextField(null=True, blank=True)