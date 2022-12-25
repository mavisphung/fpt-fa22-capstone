from rest_framework import serializers
from transaction.models import TransactionPlatform
from transaction.models import Transaction

class VnPayCreateTransactionSerializer(serializers.Serializer):
    vnp_amount = serializers.FloatField()
    vnp_BankCode = serializers.CharField()
    vnp_BankTranNo = serializers.CharField()
    vnp_TransactionNo = serializers.FloatField()
    vnp_TxnRef = serializers.CharField()
    vnp_SecureHashType = serializers.CharField()
    vnp_SecureHash = serializers.CharField()
    vnp_TransactionStatus = serializers.CharField()
    detail = serializers.JSONField()

    def create(self, validated_data):
        amount = validated_data['vnp_amount']
        bankTransactionNo = validated_data['vnp_BankTranNo']
        platformTransactionNo = validated_data['vnp_TransactionNo']
        status = validated_data['vnp_TransactionStatus']
        securerity_hash = validated_data['securerityHash']
        detail = validated_data['detail']
        security_hash_type = validated_data['securerityHash']
        order = self.context['order']
        transaction: Transaction = Transaction(
            amout = amount, 
            bankTransactionNo = bankTransactionNo, 
            status = status, 
            securerity_hash = securerity_hash, 
            detail = detail,
            security_hash_type = security_hash_type,
            platformTransactionNo = platformTransactionNo,
        )
        transaction.status = status
        transaction.platform = TransactionPlatform.VNPAY
        transaction.order = order
        transaction.save()
        return transaction


class ReadOnlyTransactionSerializer(serializers.Serializer):
    def to_representation(self, instance:Transaction):
        return {
            'id': instance.pk,
            'bankTransactionNo': instance.bankTransactionNo,
            'platformTransactionNo': instance.platformTransactionNo,
            'platform': instance.platform,
            'amount': instance.amount,
            'order': {
                'id': instance.order.pk,
                'code': instance.order.code,
                'createdAt': instance.order.createdAt,
                'currency': instance.order.currency
            },
        }
        
class CTransactionSerializer(serializers.Serializer):
    orderInfo = serializers.CharField(max_length = 255)
    platform = serializers.ChoiceField(choices = TransactionPlatform.choices)
    amount = serializers.FloatField(min_value = 0.0)
    sender = serializers.IntegerField(min_value = 1)
    receiver = serializers.IntegerField(min_value = 1)

    def to_representation(self, instance):
        
        
        return super().to_representation(instance)
    
    class Meta:
        fields = ['orderInfo', 'platform', 'amount', 'sender', 'receiver']