# Generated by Django 4.1.2 on 2022-11-07 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=64, verbose_name='service name')),
                ('description', models.CharField(max_length=255, verbose_name='service description')),
                ('price', models.FloatField(default=0.0, verbose_name='service price')),
                ('category', models.CharField(choices=[('AT_PATIENT_HOME', 'At Patient Home'), ('AT_DOCTOR_HOME', 'At Doctor Home'), ('ONLINE', 'Online')], max_length=20, verbose_name='category')),
            ],
            options={
                'db_table': 'service',
            },
        ),
    ]
