from django.db import models
from django.conf import settings
# TODO accept only precise types of activity_type

# Create your models here.
class Activity(models.Model):
    activity_type = models.CharField(max_length=30)
    start_date = models.DateField()
    description = models.TextField(blank=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)