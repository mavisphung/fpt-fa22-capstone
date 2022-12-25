from rest_framework import serializers
from disease.models import Diagnose
from disease.models import Disease
from shared.exceptions import CustomValidationError


class DiagnoseSerializer(serializers.Serializer):
    disease = serializers.IntegerField(default=1)
    record = serializers.IntegerField(default=1)
    description = serializers.CharField()

    def validate_disease(self, disease):
        object = Disease.objects.filter(pk=disease).first()
        if object is None:
            raise CustomValidationError(
                message='Invalid disease', detail='Invalid disease', code=404)
        return object

    def validate_record(self, record):
        object = Disease.objects.filter(pk=record).first()
        if object is None:
            raise CustomValidationError(
                message='Invalid record', detail='Invalid record', code=404)
        return object

    def create(self, validated_data):
        new = Diagnose(disease=validated_data['diagnose'],
                       record=validated_data['record'],
                       detail=validated_data['detail'])
        new.save()

    def to_representation(self, instance: Diagnose):
        return {
            'disease': instance.disease.name,
            'description': instance.description,
            'issueDate': instance.createdAt,
        }

class ReadOnlyDiseaseSerializer(serializers.BaseSerializer):
    
    def to_representation(self, instance: Disease):
        
        return {
            'id': instance.pk,
            'code': instance.code,
            'otherCode': instance.otherCode,
            'generalName': instance.vGeneralName,
            'diseaseName': instance.vDiseaseName,
        }