# Generated by Django 4.1.2 on 2022-12-16 17:47

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('health_record', '0010_delete_symptom'),
    ]

    operations = [
        migrations.AddField(
            model_name='healthrecord',
            name='name',
            field=models.CharField(default=uuid.uuid4, max_length=64, verbose_name='name'),
        ),
    ]
