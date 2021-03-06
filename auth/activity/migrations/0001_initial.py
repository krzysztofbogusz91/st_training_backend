# Generated by Django 3.1 on 2020-09-13 07:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercise_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ExerciseSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weights', models.IntegerField()),
                ('reps', models.IntegerField()),
                ('notes', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='StrengthSections',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_name', models.CharField(max_length=100)),
                ('exercises', models.ManyToManyField(blank=True, null=True, related_name='exercise', to='activity.Exercise')),
            ],
        ),
        migrations.AddField(
            model_name='exercise',
            name='sets',
            field=models.ManyToManyField(blank=True, null=True, related_name='exercise_set', to='activity.ExerciseSet'),
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_type', models.CharField(max_length=30)),
                ('start_date', models.DateField()),
                ('name', models.TextField(blank=True, default='text')),
                ('description', models.TextField(blank=True)),
                ('posted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('strength', models.ManyToManyField(blank=True, null=True, related_name='exercise', to='activity.StrengthSections')),
            ],
        ),
    ]
