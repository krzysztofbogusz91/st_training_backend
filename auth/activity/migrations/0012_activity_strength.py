# Generated by Django 3.1 on 2020-09-09 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0011_remove_activity_strength'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='strength',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='strength', to='activity.strengthsection'),
        ),
    ]
