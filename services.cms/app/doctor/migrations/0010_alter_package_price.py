# Generated by Django 4.0.4 on 2022-09-25 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0009_package'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='price',
            field=models.FloatField(default=0.0, verbose_name='package price'),
        ),
    ]
