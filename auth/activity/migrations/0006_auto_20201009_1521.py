# Generated by Django 3.1 on 2020-10-09 15:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0005_auto_20201009_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='strengthsections',
            name='activity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='activity.activity'),
        ),
    ]
