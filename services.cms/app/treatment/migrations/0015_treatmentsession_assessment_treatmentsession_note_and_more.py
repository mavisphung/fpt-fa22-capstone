# Generated by Django 4.0.4 on 2022-12-06 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('treatment', '0014_alter_treatmentcontract_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='treatmentsession',
            name='assessment',
            field=models.TextField(null=True, verbose_name='assessment'),
        ),
        migrations.AddField(
            model_name='treatmentsession',
            name='note',
            field=models.TextField(null=True, verbose_name='note'),
        ),
        migrations.AlterField(
            model_name='treatmentsession',
            name='checkInCode',
            field=models.CharField(default='123456', max_length=255, verbose_name='check in code'),
        ),
    ]