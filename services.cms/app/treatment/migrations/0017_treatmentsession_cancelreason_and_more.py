# Generated by Django 4.0.4 on 2022-12-06 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('treatment', '0016_alter_treatmentsession_assessment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='treatmentsession',
            name='cancelReason',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='cancellation reason'),
        ),
        migrations.AddField(
            model_name='treatmentsession',
            name='isDoctorCancelled',
            field=models.BooleanField(default=False, verbose_name='Is_Doctor_Cancel'),
        ),
        migrations.AddField(
            model_name='treatmentsession',
            name='isSupervisorCancelled',
            field=models.BooleanField(default=False, verbose_name='Is_Supervisor_Cancel'),
        ),
        migrations.AddField(
            model_name='treatmentsession',
            name='isSystemCancelled',
            field=models.BooleanField(default=False, verbose_name='Is_System_Cancel'),
        ),
    ]
