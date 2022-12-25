# Generated by Django 4.1.2 on 2022-11-24 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='securerity_hash',
        ),
        migrations.AddField(
            model_name='transaction',
            name='security_hash',
            field=models.CharField(max_length=520, null=True, verbose_name='security hash'),
        ),
        migrations.AlterField(
            model_name='order',
            name='code',
            field=models.CharField(max_length=255, verbose_name='code'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.FloatField(default=0, verbose_name='amount'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='bankTransactionNo',
            field=models.CharField(max_length=255, null=True, verbose_name='bank transaction no.'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='platform',
            field=models.CharField(choices=[('MOMO', 'Momo'), ('VNPAY', 'Vnpay'), ('CASH', 'Cash')], default='VNPAY', max_length=20, verbose_name='platform'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='platformTransactionNo',
            field=models.CharField(max_length=255, null=True, verbose_name='platform transaction no.'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='security_hash_type',
            field=models.CharField(max_length=20, null=True, verbose_name='hash type'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.CharField(choices=[('SUCCESS', 'Success'), ('FAIL', 'Fail'), ('ROLLBACK', 'Rollback'), ('REFUNDED', 'Refunded')], default='FAIL', max_length=15, verbose_name='transaction status'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='type',
            field=models.CharField(choices=[('RECHARGED', 'Recharged'), ('TRANSFER', 'Transferred'), ('WITHDRAWED', 'Withdrawed'), ('REFUNDED', 'Refunded')], default='RECHARGED', max_length=20, verbose_name='type'),
        ),
        migrations.AlterModelTable(
            name='order',
            table='order',
        ),
    ]