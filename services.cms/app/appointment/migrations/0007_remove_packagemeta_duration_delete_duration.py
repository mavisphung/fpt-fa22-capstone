# Generated by Django 4.0.4 on 2022-09-12 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0006_appointment_isdoctorcancelled_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='packagemeta',
            name='duration',
        ),
        migrations.DeleteModel(
            name='Duration',
        ),
    ]
