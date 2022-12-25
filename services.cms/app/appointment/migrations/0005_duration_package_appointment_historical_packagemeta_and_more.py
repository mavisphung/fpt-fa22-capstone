# Generated by Django 4.0.4 on 2022-09-08 13:16

import appointment.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0004_appointment_diseasedescription'),
    ]

    operations = [
        migrations.CreateModel(
            name='Duration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('interval', models.IntegerField(verbose_name='interval')),
            ],
            options={
                'db_table': 'duration',
            },
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, verbose_name='package name')),
                ('description', models.CharField(max_length=512, verbose_name='package description')),
            ],
            options={
                'db_table': 'package',
            },
        ),
        migrations.AddField(
            model_name='appointment',
            name='historical',
            field=models.JSONField(default=appointment.models._get_default_value, verbose_name='historical detail'),
        ),
        migrations.CreateModel(
            name='PackageMeta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('price', models.FloatField(default=0.0, verbose_name='price')),
                ('duration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='package_metas', to='appointment.duration')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='package_metas', to='appointment.package')),
            ],
            options={
                'db_table': 'package_meta',
            },
        ),
        migrations.AddField(
            model_name='appointment',
            name='package_meta',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='appointments', to='appointment.packagemeta'),
        ),
    ]