# Generated by Django 4.0.4 on 2022-06-24 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='isApproved',
            field=models.BooleanField(default=True, verbose_name='is approved'),
        ),
    ]
