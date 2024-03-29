# Generated by Django 4.0.4 on 2022-12-06 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('treatment', '0013_treatmentsession_doctor_treatmentsession_patient_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='treatmentcontract',
            name='status',
            field=models.CharField(choices=[('APPROVED', 'Approved'), ('IN_PROGRESS', 'In Progress'), ('EXPIRED', 'Expired'), ('PENDING', 'Pending'), ('CANCELLED', 'Cancelled'), ('POSTPONE', 'Postpone'), ('SIGNED', 'Signed')], default='PENDING', max_length=20, verbose_name='contract status'),
        ),
    ]
