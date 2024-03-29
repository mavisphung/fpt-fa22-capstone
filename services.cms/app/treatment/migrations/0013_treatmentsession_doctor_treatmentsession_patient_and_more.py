# Generated by Django 4.0.4 on 2022-12-06 06:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0015_alter_package_isapproved'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('patient', '0002_alter_patient_supervisor'),
        ('treatment', '0012_remove_treatmentsession_doctor_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='treatmentsession',
            name='doctor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='treatment_sessions', to='doctor.doctor'),
        ),
        migrations.AddField(
            model_name='treatmentsession',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='treatment_sessions', to='patient.patient'),
        ),
        migrations.AddField(
            model_name='treatmentsession',
            name='supervisor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='treatment_sessions', to=settings.AUTH_USER_MODEL),
        ),
    ]
