# Generated by Django 4.0.4 on 2022-12-06 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('treatment', '0015_treatmentsession_assessment_treatmentsession_note_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='treatmentsession',
            name='assessment',
            field=models.JSONField(default={}, verbose_name='assessment'),
        ),
        migrations.AlterField(
            model_name='treatmentsession',
            name='note',
            field=models.JSONField(default={}, verbose_name='note'),
        ),
    ]