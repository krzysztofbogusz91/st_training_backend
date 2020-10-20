from rest_framework import serializers

from .models import Activity, CardioSession, Exercise, ExerciseSet, StrengthSections


class ExerciseSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseSet
        fields = ['id', 'weights', 'reps', 'notes']

class ExercisesSerializer(serializers.ModelSerializer):
    sets = ExerciseSetSerializer(many=True, read_only=True)
    
    class Meta:
        model = Exercise
        fields = ['id', 'exercise_name', 'sets']

class SectionSerializer(serializers.ModelSerializer):
    exercises = ExercisesSerializer(many=True, read_only=True)
    
    class Meta:
        model = StrengthSections
        fields = ['id', 'section_name', 'exercises']


class ActivitySerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = Activity
        fields = ['activity_type', 'start_date', 'name',
        'description', 'posted_by', 'cardio', 'sections']
