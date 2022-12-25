# Generated by Django 4.0.4 on 2022-10-04 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('doctor', '0011_package_category'),
        ('patient', '0002_alter_patient_supervisor'),
        ('health_record', '0005_patienthealthrecord_patientmedicalhistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicalInstruction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('requirments', models.JSONField(verbose_name='requirments')),
                ('submissions', models.CharField(max_length=300, null=True, verbose_name='submissions')),
                ('status', models.TextField(choices=[('PENDING', 'Pending'), ('COMPLETED', 'Completed'), ('CANCELLED', 'Cancelled')], default='PENDING', max_length=100, verbose_name='status')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MedicalInstructionCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MedicalInstructionFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('message', models.CharField(max_length=300, null=True, verbose_name='message')),
                ('attachment', models.CharField(max_length=300, null=True, verbose_name='attachment')),
                ('instruction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='instruction.medicalinstruction')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='medicalinstruction',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='medical_instructions', to='instruction.medicalinstructioncategory'),
        ),
        migrations.AddField(
            model_name='medicalinstruction',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medical_instructions', to='doctor.doctor'),
        ),
        migrations.AddField(
            model_name='medicalinstruction',
            name='healthRecord',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medical_instructions', to='health_record.healthrecord'),
        ),
        migrations.AddField(
            model_name='medicalinstruction',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medical_instructions', to='patient.patient'),
        ),
    ]