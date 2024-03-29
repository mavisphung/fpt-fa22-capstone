# Generated by Django 4.0.4 on 2022-08-19 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disease', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disease',
            name='code',
            field=models.CharField(max_length=10, null=True, verbose_name='code'),
        ),
        migrations.AlterField(
            model_name='disease',
            name='diseaseName',
            field=models.CharField(max_length=255, null=True, verbose_name='disease name'),
        ),
        migrations.AlterField(
            model_name='disease',
            name='generalName',
            field=models.CharField(max_length=255, null=True, verbose_name='general name'),
        ),
        migrations.AlterField(
            model_name='disease',
            name='otherCode',
            field=models.CharField(max_length=10, null=True, verbose_name='other code'),
        ),
        migrations.AlterField(
            model_name='disease',
            name='vDiseaseName',
            field=models.CharField(max_length=255, null=True, verbose_name='vietnamese disease name'),
        ),
        migrations.AlterField(
            model_name='disease',
            name='vGeneralName',
            field=models.CharField(max_length=255, null=True, verbose_name='vietnamese general name'),
        ),
    ]
