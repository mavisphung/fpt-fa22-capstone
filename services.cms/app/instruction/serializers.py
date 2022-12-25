from django.utils import timezone
from rest_framework import serializers
from shared.utils import to_json
from doctor.models import Doctor
from doctor.serializers import DoctorSerializer
from patient.models import Patient
from patient.serializers import PatientSerializer
from health_record.models import HealthRecord
from instruction.models import MedicalInstruction, MedicalInstructionCategory, MedicalInstructionStatus
from shared.exceptions import CustomValidationError
from django.db import transaction
from myapp.settings import DATETIME_FORMAT

from shared.utils import from_json
import logging
logger  = logging.getLogger(__name__)
class CreateInstructionSerializerList(serializers.ListSerializer):
    doctor = serializers.IntegerField(default= 1)
    requirments = serializers.JSONField(default={})
    status = serializers.CharField(default = MedicalInstructionStatus.COMPLETED)
    category = serializers.IntegerField(default= 1)

    @transaction.atomic()
    def create(self, validated_data):    
        context: dict = self.context
        healthRecord: HealthRecord = context.get('healthRecord', None)
        patient = context.get('patient', None)
        healthRecord.save()
        details = []
        for item in validated_data:
            item['patient'] = patient,
            item['doctor'] = healthRecord.doctor
            details.append(
                MedicalInstruction(
                    healthRecord = healthRecord,
                    patient = patient, 
                    doctor = item['doctor'], 
                    requirments = to_json(item['requirments']), 
                    submissions = item.get('submission', ''),
                    category = item['category'],
                    status = item.get('status',MedicalInstructionStatus.COMPLETED)
                )
            )
        return MedicalInstruction.objects.bulk_create(details)
class UpdateMedicalInstructionSerializer(serializers.Serializer):
    submissions = serializers.CharField(required=False)
    def update(self, instance, validated_data):
        instruction: MedicalInstruction = instance
        action:str= self.context['action']
        if instruction.status != MedicalInstructionStatus.PENDING:
            raise CustomValidationError(message='Invalid Action', detail='Medical Instruction must be pending to perform this action', code=400)
        if action.lower() == 'cancel':
            instruction.status = MedicalInstructionStatus.CANCELLED
        if action.lower() == 'submit':
            instruction.status = MedicalInstructionStatus.COMPLETED
            instruction.submissions = validated_data['submissions']
        instruction.save()
        return instruction
    
    def to_representation(self, instance: MedicalInstruction):
        patient = PatientSerializer(instance=instance.patient)
        doctor:DoctorSerializer = DoctorSerializer(instance=instance.doctor)
        return {
            "id": instance.pk,
            "patient": patient.data,
            'doctor': doctor.data,
            'createdAt': instance.createdAt,
            'category': instance.category.name,
            'requirement': to_json(instance.requirments),
            'status': instance.status,
            'submissions':  to_json(instance.submissions),
        }

class ReadOnlyMedicalInstructionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            "id": instance.pk,
            'createdAt': instance.createdAt.strftime(DATETIME_FORMAT),
            'category': instance.category.name,
            'requirments': instance.requirments,
            'status': instance.status,
            'submissions': instance.submissions,
        }


class ReadOnlyDoctorMedicalInstructionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            "id": instance.pk,
            'createdAt': instance.createdAt.strftime(DATETIME_FORMAT) if instance.createdAt else None,
            'category': instance.category.name,
            'requirement': instance.requirments,
            'submissions': instance.submissions,
            'status': instance.status
        }

class InstructionCateSerializer(serializers.BaseSerializer):
    
    def to_representation(self, instance: MedicalInstructionCategory):
        return {
            'id': instance.pk,
            'name': instance.name,
        }


class CreateInstructionSerializer(serializers.Serializer):
    healthRecord = serializers.IntegerField(default=1)
    doctor = serializers.IntegerField(default=1)
    patient = serializers.IntegerField(default=1)
    category = serializers.IntegerField(default=1)
    requirments = serializers.JSONField()
    status = serializers.CharField(required= False)

    def validate_doctor(self, doctor):
        result = Doctor.objects.filter(pk=doctor).first()
        if result is None:
            raise CustomValidationError(
                message='Doctor Not Found', detail='Doctor is not exist', code=404)
        if not result.isApproved:
            raise CustomValidationError(
                message='Invalid Action', detail='Doctor needed to be approve by system to perfrom this action', code=400)
        return result

    def validate_category(self, category):
        result = MedicalInstructionCategory.objects.filter(pk = category).first()
        return result

    def validate_patient(self, patient):
        result = Patient.objects.filter(pk=patient).first()
        if result is None:
            raise CustomValidationError(
                message='Patient Not Found', detail='Không tìm thấy hồ sơ bệnh nhân', code=404)
        return result

    def validate_healthRecord(self, healthRecord):
        result = HealthRecord.objects.filter(pk=healthRecord).first()
        if result is None:
            raise CustomValidationError(
                message='Health record not found', detail='Không tìm thấy hồ sơ bệnh án', code=404)
        return result

    def create(self, validated_data):
        logger.info('single instruction invoked...')
        healthRecord: HealthRecord = validated_data['healthRecord']
        doctor = validated_data['doctor']
        patient = validated_data['patient']
        endDate = timezone.now().replace(day = healthRecord.endedAt.day, month = healthRecord.endedAt.month , year = healthRecord.endedAt.year, hour = 23, minute = 59, second = 59)
        if healthRecord.doctor != doctor:
            raise CustomValidationError(
                message='Invalid Action', detail='Doctor is not belong to health record', code=400)
        if healthRecord.patient != patient:
            raise CustomValidationError(
                message='Invalid Action', detail='Patient is not belong to health record', code=400)
        
        if endDate < timezone.now():
            raise CustomValidationError(
                message='Invalid Action', detail='Health Record is closed', code=400)
        insturction = MedicalInstruction(**validated_data)
        insturction.patient = healthRecord.patient
        insturction.save()
        return insturction

    def to_representation(self, instance: MedicalInstruction):
        patient = PatientSerializer(instance=instance.patient)
        doctor:DoctorSerializer = DoctorSerializer(instance=instance.doctor)
        return {
            "id": instance.pk,
            "patient": patient.data,
            'doctor': {
                'doctorId': doctor.data['id'],
                'email': doctor.data['email'],
                'Full Name': doctor.data['firstName'] + ' ' + doctor.data['lastName'],
            },
            'createdAt': instance.createdAt,
            'category': instance.category.name,
            'requirement': from_json(instance.requirments),
            'submissions': from_json(instance.submissions),
            'status': instance.status,
            'healthRecord': instance.healthRecord.pk
        }

    class Meta:
        list_serializer_class = CreateInstructionSerializerList


class HealthRecordInstructionSerializer(serializers.Serializer):
    requirments = serializers.JSONField(default = {})
    status = serializers.CharField(required= False)
    category = serializers.IntegerField(required= False)

    def validate_category(self, category):
        category = MedicalInstructionCategory.objects.filter(pk = category).first()
        if category is None:
            raise CustomValidationError('CATEGORY_NOT_FOUND', 'Category for instruction not found', code = 400)
        return category

    def to_representation(self, instance):
        logger.info('invoke to_representation')
        patient = PatientSerializer(instance=instance.patient)
        doctor:DoctorSerializer = DoctorSerializer(instance=instance.doctor)
        return {
            "id": instance.pk,
            "patient": patient.data,
            'doctor': {
                'doctorId': doctor.data['id'],
                'email': doctor.data['email'],
                'Full Name': doctor.data['firstName'] + ' ' + doctor.data['lastName'],
            },
            'createdAt': instance.createdAt,
            'category': instance.category.name,
            'requirement': from_json(instance.requirments),
            'submissions': from_json(instance.submissions),
            'status': instance.status,
            'healthRecord': instance.healthRecord.pk
        }
    class Meta:
        list_serializer_class = CreateInstructionSerializerList