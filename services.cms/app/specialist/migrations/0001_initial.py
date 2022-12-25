# Generated by Django 4.0.4 on 2022-09-11 08:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('doctor', '0008_remove_workingshift_time_workingshift_endtime_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Specialist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=64, null=True, verbose_name='specialist name')),
                ('description', models.CharField(max_length=255, null=True, verbose_name='description')),
            ],
            options={
                'db_table': 'specialist',
            },
        ),
        migrations.CreateModel(
            name='DoctorSpecialist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specialists', to='doctor.doctor')),
                ('specialist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctors', to='specialist.specialist')),
            ],
            options={
                'db_table': 'doctor_specialist',
            },
        ),
    ]
