from rest_framework import serializers
from user.models import User
from shared.models import Gender
from patient.models import Patient
from myapp.settings import DOB_FORMAT
from django.db import transaction

keys_to_remove = ('_state', 'createdAt', 'updatedAt', )

class PatientSerializer(serializers.Serializer):
    firstName = serializers.CharField(max_length = 32)
    lastName = serializers.CharField(max_length = 32)
    dob = serializers.DateField(required = False)
    address = serializers.CharField(max_length = 255)
    gender = serializers.ChoiceField(choices = Gender.choices)
    avatar = serializers.CharField(max_length = 255)
    
    
    @transaction.atomic
    def create(self, validated_data):
        user: User = self.context.get('user')
        patient = Patient(**validated_data, supervisor = user)
        patient.save()
        return patient
    
    @transaction.atomic
    def update(self, instance: Patient, validated_data: dict):
        update_fields = ['updatedAt']
        for key, value in validated_data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
                update_fields.append(key)
                
        instance.save(update_fields = update_fields)
        return instance
    
    def to_representation(self, instance: Patient) -> dict:
        data = instance.__dict__
        for key in keys_to_remove:
            del data[key]
        
        dob = data.get('dob', None)
        if dob:
            data['dob'] = dob.strftime(DOB_FORMAT)
        return data
        # return super().to_representation(instance)
    
    class Meta:
        fields = ['firstName', 'lastName', 'dob', 'address', 'gender', 'avatar']

class UpdatePatientSerializer(PatientSerializer):
    id = serializers.IntegerField(min_value = 1)
    
    class Meta:
        fields = ['id', 'firstName', 'lastName', 'dob', 'address', 'gender', 'avatar']