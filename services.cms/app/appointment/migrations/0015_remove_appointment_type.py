# Generated by Django 4.1.2 on 2022-10-21 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0014_appointment_issystemcancelled'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='type',
        ),
    ]