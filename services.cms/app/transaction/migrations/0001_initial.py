# Generated by Django 4.0.4 on 2022-11-01 14:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import transaction.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=25, verbose_name='code')),
                ('amount', models.FloatField(verbose_name='amount')),
                ('currency', models.CharField(max_length=20, verbose_name='currency')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('amount', models.FloatField(verbose_name='Amount')),
                ('type', models.TextField(choices=[('RECHARGED', 'Recharged'), ('TRANSFER', 'Transferred'), ('WITHDRAWED', 'Withdrawed'), ('REFUNDED', 'Refunded')], default='RECHARGED', verbose_name='Type')),
                ('platform', models.TextField(choices=[('MOMO', 'Momo'), ('VNPAY', 'Vnpay'), ('CASH', 'Cash')], default='VNPAY', verbose_name='Platform')),
                ('bankTransactionNo', models.CharField(max_length=50, null=True, verbose_name='bank_transaction_no')),
                ('platformTransactionNo', models.TextField(max_length=50, null=True, verbose_name='platform_transaction_no')),
                ('status', models.CharField(max_length=10, verbose_name='transaction_status')),
                ('security_hash_type', models.CharField(max_length=20, verbose_name='hash_type')),
                ('securerity_hash', models.CharField(max_length=520, verbose_name='securerity_hash')),
                ('detail', models.JSONField(default=transaction.models._get_default_value, verbose_name='platform details')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='transactions', to='transaction.order')),
                ('receiver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='in_transactions', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='out_transactions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
