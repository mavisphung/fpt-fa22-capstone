from rest_framework import serializers
from user.models import User, UserType
from shared.exceptions import CustomValidationError
from shared.response_messages import ResponseMessage

class DepositSerializer(serializers.Serializer):
    amount = serializers.FloatField(min_value = 1000.0)
    
    def create(self, validated_data: dict):
        account: User = self.context.get('account')
        amount: float = validated_data.get('amount')
        # TODO: Add transaction to this
        account.mainBalance += amount
        account.save(update_fields = ['updatedAt', 'mainBalance'])
        return account
    
    def to_representation(self, instance: User):
        ''''id', 'email', 'firstName', 
            'lastName', 'type', 'address', 
            'gender', 'phoneNumber', 'avatar', 'tempBalance', 'mainBalance', 'doctorId'
        '''
        data = {
            'id': instance.pk,
            'email': instance.email,
            'firstName': instance.firstName,
            'lastName': instance.lastName,
            'type': instance.type,
            'address': instance.address,
            'gender': instance.gender,
            'phoneNumber': instance.phoneNumber,
            'avatar': instance.avatar,
            'tempBalance': instance.tempBalance,
            'mainBalance': instance.mainBalance,
        }
        if instance.type == UserType.DOCTOR:
            data['doctorId'] = instance.doctor_id
            
        return data
    
    class Meta:
        fields = ['amount']
        
class WithdrawalSerializer(DepositSerializer):
    
    def create(self, validated_data: dict):
        account: User = self.context.get('account')
        amount: float = validated_data.get('amount')
        # TODO: Add transaction to this
        if account.mainBalance <= amount:
            raise CustomValidationError(
                message = ResponseMessage.WALLET_LESS_THAN_INPUT
            )
        account.mainBalance -= amount
        account.save(update_fields = ['updatedAt', 'mainBalance'])
        return account