# Generated by Django 4.0.4 on 2022-06-28 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0003_doctor_age'),
    ]

    operations = [
        migrations.CreateModel(
            name='Specification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('url', models.CharField(max_length=255, verbose_name='url')),
                ('type', models.CharField(choices=[('IMG', 'Img'), ('FILE', 'File'), ('PDF', 'Pdf')], max_length=10, verbose_name='spec type')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specs', to='doctor.doctor')),
            ],
            options={
                'db_table': 'specification',
            },
        ),
    ]
