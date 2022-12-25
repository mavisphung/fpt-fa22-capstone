# Generated by Django 4.0.4 on 2022-09-09 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0005_duration_package_appointment_historical_packagemeta_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='isDoctorCancelled',
            field=models.BooleanField(default=False, verbose_name='doctor cancelled'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='isSupervisorCancelled',
            field=models.BooleanField(default=False, verbose_name='supervisor cancelled'),
        ),
    ]