from django.contrib import admin
from activity.models import Activity, StrengthSections, Exercise, ExerciseSet
# Register your models here.
admin.site.register(Activity)
admin.site.register(StrengthSections)
admin.site.register(Exercise)
admin.site.register(ExerciseSet)