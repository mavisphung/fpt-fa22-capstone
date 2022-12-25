from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from user.models import User
from shared.models import BaseModel
from django.utils.translation import gettext_lazy as _
def _get_default_value():
    return {}

class TransactionType(models.TextChoices):
    RECHARGED = 'RECHARGED'
    TRANSFERRED = 'TRANSFER'
    WITHDRAWED = 'WITHDRAWED'
    REFUNDED = 'REFUNDED'


class TransactionPlatform(models.TextChoices):
    MOMO = 'MOMO'
    VNPAY = 'VNPAY'
    CASH = 'CASH',
    SYSTEM = 'SYSTEM',

class TransactionStatus(models.TextChoices):
    SUCCESS = 'SUCCESS'
    FAIL = 'FAIL'
    ROLLBACK = 'ROLLBACK'
    REFUNDED = 'REFUNDED'

class Order(BaseModel):
    code = models.CharField(_('code'), max_length = 255)
    amount = models.FloatField(_('amount'))
    currency = models.CharField(_('currency'), max_length = 20)
    content_type = models.ForeignKey(ContentType, on_delete = models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        db_table = 'order'

class Transaction(BaseModel):
    amount  = models.FloatField(_('amount'), default = 0)
    type = models.CharField(
        _('type'), 
        max_length = 20,
        choices = TransactionType.choices, 
        default = TransactionType.RECHARGED
    )
    platform = models.CharField(
        _('platform'), 
        max_length = 20,
        choices = TransactionPlatform.choices, 
        default = TransactionPlatform.VNPAY
    )
    bankTransactionNo = models.CharField(_('bank transaction no.'), max_length = 255, null = True)
    platformTransactionNo = models.CharField(_('platform transaction no.'), max_length = 255, null = True)
    status = models.CharField(
        _('transaction status'), 
        max_length = 15, 
        choices = TransactionStatus.choices,
        default = TransactionStatus.FAIL
    )
    security_hash_type = models.CharField(_('hash type'), max_length = 20, null = True)
    security_hash = models.CharField(_('security hash'), max_length = 520, null = True)
    detail = models.JSONField(_('platform details'), default=_get_default_value)

    order = models.ForeignKey(
        Order,
        related_name = 'transactions',
        on_delete = models.RESTRICT,
        null = True
    )
    sender = models.ForeignKey(
        User, 
        related_name = 'out_transactions', 
        on_delete=models.RESTRICT, 
        null = True
    )
    receiver = models.ForeignKey(
        User, 
        related_name = 'in_transactions' , 
        on_delete=models.RESTRICT, 
        null = True
    )
