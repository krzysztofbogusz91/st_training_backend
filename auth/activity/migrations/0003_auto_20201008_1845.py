# Generated by Django 3.1 on 2020-10-08 18:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0002_auto_20201008_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='cardio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='activity.cardiosession'),
        ),
        migrations.RemoveField(
            model_name='activity',
            name='strength',
        ),
        migrations.AddField(
            model_name='activity',
            name='strength',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exercise', to='activity.strengthsections'),
        ),
        migrations.RemoveField(
            model_name='exercise',
            name='sets',
        ),
        migrations.AddField(
            model_name='exercise',
            name='sets',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exercise_set', to='activity.exerciseset'),
        ),
        migrations.RemoveField(
            model_name='strengthsections',
            name='exercises',
        ),
        migrations.AddField(
            model_name='strengthsections',
            name='exercises',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exercise', to='activity.exercise'),
        ),
    ]
