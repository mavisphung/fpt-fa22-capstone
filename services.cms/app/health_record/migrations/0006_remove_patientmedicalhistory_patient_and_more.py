# Generated by Django 4.0.4 on 2022-10-07 02:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('health_record', '0005_patienthealthrecord_patientmedicalhistory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patientmedicalhistory',
            name='patient',
        ),
        migrations.RemoveField(
            model_name='patientmedicalhistory',
            name='record',
        ),
        migrations.DeleteModel(
            name='PatientHealthRecord',
        ),
        migrations.DeleteModel(
            name='PatientMedicalHistory',
        ),
    ]
