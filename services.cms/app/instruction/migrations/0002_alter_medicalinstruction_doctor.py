# Generated by Django 4.0.4 on 2022-12-15 00:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0016_alter_doctor_firstname_alter_doctor_lastname'),
        ('instruction', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicalinstruction',
            name='doctor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='medical_instructions', to='doctor.doctor'),
        ),
    ]