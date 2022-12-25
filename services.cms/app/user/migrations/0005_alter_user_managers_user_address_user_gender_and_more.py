# Generated by Django 4.0.4 on 2022-06-19 02:59

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_remove_user_username'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', user.models.CustomUserManager()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(blank=True, max_length=255, verbose_name='address'),
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('OTHER', 'Other')], default='OTHER', max_length=10, verbose_name='gender'),
        ),
        migrations.AddField(
            model_name='user',
            name='phoneNumber',
            field=models.CharField(blank=True, max_length=20, verbose_name='phone number'),
        ),
        migrations.AlterField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('ADMIN', 'Admin'), ('MEMBER', 'Member'), ('DOCTOR', 'Doctor'), ('PATIENT', 'Patient')], default='MEMBER', max_length=10, verbose_name='user type'),
        ),
    ]