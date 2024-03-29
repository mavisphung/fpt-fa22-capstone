# Generated by Django 4.0.4 on 2022-08-01 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HealthRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('startedAt', models.DateField(auto_now_add=True, verbose_name='started date')),
                ('endedAt', models.DateField(null=True, verbose_name='ended date')),
                ('isPatientProvided', models.BooleanField(default=False, verbose_name='is provided by patient')),
            ],
            options={
                'db_table': 'health_record',
            },
        ),
    ]
