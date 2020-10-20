# Generated by Django 3.1 on 2020-10-08 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0003_auto_20201008_1845'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='strength',
        ),
        migrations.AddField(
            model_name='activity',
            name='strength',
            field=models.ManyToManyField(blank=True, related_name='exercise', to='activity.StrengthSections'),
        ),
        migrations.RemoveField(
            model_name='exercise',
            name='sets',
        ),
        migrations.AddField(
            model_name='exercise',
            name='sets',
            field=models.ManyToManyField(blank=True, related_name='exercise_set', to='activity.ExerciseSet'),
        ),
        migrations.RemoveField(
            model_name='strengthsections',
            name='exercises',
        ),
        migrations.AddField(
            model_name='strengthsections',
            name='exercises',
            field=models.ManyToManyField(blank=True, related_name='exercise', to='activity.Exercise'),
        ),
    ]