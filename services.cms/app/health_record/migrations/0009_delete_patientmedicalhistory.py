# Generated by Django 4.0.4 on 2022-10-13 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('health_record', '0008_merge_20221013_1550'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PatientMedicalHistory',
        ),
    ]