# Generated by Django 4.1.2 on 2022-11-21 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0004_service_method_alter_service_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='is deleted'),
        ),
    ]