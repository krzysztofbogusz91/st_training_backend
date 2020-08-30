from django.db import models

# TODO accept only precise types of activity_type

# Create your models here.
class Activity(models.Model):
    activity_type = models.CharField(max_length=30)
    start_date = models.DateField()
    description = models.TextField(blank=True)