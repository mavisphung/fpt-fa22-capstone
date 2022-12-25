# Generated by Django 4.0.4 on 2022-08-04 11:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('patient', '0002_alter_patient_supervisor'),
        ('doctor', '0005_doctor_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('beginAt', models.DateTimeField()),
                ('endAt', models.DateTimeField()),
                ('status', models.CharField(choices=[('COMPLETED', 'Completed'), ('CANCELLED', 'Cancelled'), ('IN_PROGRESS', 'In Progress'), ('PENDING', 'Pending')], default='PENDING', max_length=15, verbose_name='status')),
                ('checkInCode', models.CharField(max_length=255, unique=True)),
                ('cancelReason', models.TextField(null=True, verbose_name='cancellation reason')),
                ('booker', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='appointments', to=settings.AUTH_USER_MODEL)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='appointments', to='doctor.doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='appointments', to='patient.patient')),
            ],
            options={
                'db_table': 'appointment',
            },
        ),
    ]