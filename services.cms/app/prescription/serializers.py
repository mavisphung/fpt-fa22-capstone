from datetime import datetime
from rest_framework import serializers
from doctor.models import Doctor
from health_record.models import HealthRecord
from instruction import models
from medicine.models import Medicine
from patient.models import Patient
from prescription.models import PrescriptionDetail
from shared.exceptions import CustomValidationError
from prescription.models import Prescription, PrescriptionDetail
from django.db import transaction

from shared.utils import from_json, to_json


class PrescriptionDetailReadOnlySerializer(serializers.BaseSerializer):
    def to_representation(self, instance: PrescriptionDetail):
        return {
            'medicineId': instance.medicine_id,
            'medicine': instance.medicine.name,
            'usage': instance.guide,
            'quantity': instance.quantity,
            'unit': instance.unit
        }


class PrescriptionDetailListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        context: dict = self.context
        prescription = context['prescription']
        prescription.save()
        details = []
        for item in validated_data:
            item['prescription'] = context['prescription']
            details.append(PrescriptionDetail(**item))
        return PrescriptionDetail.objects.bulk_create(details)
class PrescriptionDetailSerializer(serializers.Serializer):
    medicine = serializers.IntegerField(default=1)
    guide = serializers.CharField()
    quantity = serializers.IntegerField(default=0, required=False)
    unit = serializers.CharField(required=False)

    def validate_medicine(self, medicine):
        result = Medicine.objects.filter(pk=medicine).first()
        if result is None:
            raise CustomValidationError(
                message='Medicine Not Found', detail=f'Not found medicine with id {id}', code=404)
        return result

    def validate_guide(self, guide):
        if not guide:
            raise CustomValidationError(
                message='Guide Not Found', detail=f'Guide is not provided', code=404)
        return guide

    def to_representation(self, instance:PrescriptionDetail):
        return {
            "medicine": instance.medicine.name,
            "guide": instance.guide,
            "quantity": instance.quantity,
            "unit": instance.unit
        }

    class Meta:
        list_serializer_class = PrescriptionDetailListSerializer


class PrescriptionSerializer(serializers.Serializer):
    healthRecord = serializers.IntegerField(min_value=1)
    patient = serializers.IntegerField(min_value=1)
    fromDate = serializers.DateField()
    toDate = serializers.DateField()
    diagnose =  serializers.JSONField()
    note = serializers.JSONField(required=False)

    def validate_fromDate(self, fromDate: datetime.date):
        if datetime.now().date() > fromDate:
            raise CustomValidationError(
                message='From Date Is Past', detail=f'From Date is past from now', code=404)
        return fromDate

    def validate_toDate(self, toDate: datetime.date):
        if datetime.now().date() > toDate:
            raise CustomValidationError(
                message='Expire Date Is Past', detail=f'Expire Date is past from now', code=404)
        return toDate

    def validate_healthRecord(self, healthRecord):
        result = HealthRecord.objects.filter(
            pk=healthRecord, doctor=self.context['doctor']).first()
        if result is None:
            raise CustomValidationError(
                message='Health Record Not Found', detail=f'Not found health record with id {id}', code=404)
        return result

    def validate_patient(self, patient):
        result = Patient.objects.filter(pk=patient).first()
        if result is None:
            raise CustomValidationError(
                message='Patient Not Found', detail=f'Not found patient with id {id}', code=404)
        return result

    @transaction.atomic
    def create(self, validated_data):
        healthRecord: HealthRecord = validated_data['healthRecord']
        doctor: Doctor = self.context['doctor']
        patient: Patient = validated_data['patient']
        if validated_data['fromDate'] > validated_data['toDate']:
            raise CustomValidationError(
                message='Invalid Expire Date', detail=f'Expire Date must be greater than From Date', code=400)
        if healthRecord.doctor.pk != doctor.pk:
            raise CustomValidationError(
                message='Wrong Doctor', detail=f'Health Record is not belong to doctor', code=404)
        if healthRecord.patient.pk != patient.pk:
            raise CustomValidationError(
                message='Wrong Patient', detail=f'Health Record is not belong to patient', code=404)

        prescription: Prescription = Prescription(healthRecord=healthRecord, doctor=doctor, patient=patient,
                                                  fromDate=validated_data['fromDate'],
                                                  toDate=validated_data['toDate'],
                                                  diagnose = to_json(validated_data['diagnose']))
        detail = self.context['detail']
        if detail is not None:
            with transaction.atomic():
                detailSerializer = PrescriptionDetailSerializer(data=detail, context={
                    'prescription': prescription,
                }, many=True)
                detailSerializer.is_valid(raise_exception=True)
                detailSerializer.save()
                self.context['details'] = detailSerializer.data
        prescription.note = to_json(validated_data['note'])
        return prescription

    def to_representation(self, instance: Prescription):
        return {
            'id': instance.pk,
            'createdAt': instance.createdAt,
            'fromDate': instance.fromDate,
            'toDate': instance.toDate,
            'status': instance.cancelReason,
            'diagnose':from_json(instance.diagnose),
            'note':  from_json(instance.note) if instance.note else [] 
        }


class ReadOnlyPrepsciotionSerializer(serializers.BaseSerializer):
    def to_representation(self, instance:Prescription):
        detail = PrescriptionDetailSerializer(instance = instance.prescriptiondetail_set.all(), many= True)
        print('presentation')
        return {
            'id': instance.pk,
            'createdAt': instance.createdAt,
            'fromDate': instance.fromDate,
            'toDate': instance.toDate,
            'cancelReason': instance.cancelReason,
            'details': detail.data,
            'healthRecord': instance.healthRecord.pk,
            'diagnose': from_json(instance.diagnose),
            'doctor': {
                'id: instance.doctor': instance.doctor.pk
            }
        }


class ReadOnlyPrescriptionDetailSerializer2(serializers.BaseSerializer):
    def to_representation(self, instance: PrescriptionDetail):
        return {
            "medicine": instance.medicine.name,
            "guide": instance.guide,
            "quantity": instance.quantity,
            "unit": instance.unit
        }


class ReadOnlyPrescriptionSerializer2(serializers.BaseSerializer):
    def to_representation(self, instance: Prescription):
        detailsSerializer = ReadOnlyPrescriptionDetailSerializer2(
            instance.prescriptiondetail_set.all(), many=True)
        return {
            'id': instance.pk,
            'createdAt': instance.createdAt,
            'fromDate': instance.fromDate,
            'toDate': instance.toDate,
            'cancelReason': instance.cancelReason,
            'details': detailsSerializer.data,
            'note': instance.note,
            'healthRecord': instance.healthRecord_id,
            'doctor': instance.doctor.pk
        }


class PrescriptionUpdateSerializer(serializers.Serializer):
    cancelReason = serializers.CharField(required = False)
    @transaction.atomic
    def update(self, instance:Prescription, validated_data):
        doctor: Doctor = self.context['doctor']
        endDate = instance.healthRecord.endedAt if instance.healthRecord.endedAt else None
        if instance.doctor != doctor:
            raise CustomValidationError("Hành động không hợp lệ", "Đơn thuốc không cùng bác sĩ", code = 400)
        if instance.cancelReason == None or instance.cancelReason == '':
            raise CustomValidationError("Hành động không hợp lệ", "Cần cung cấp lí do hủy đơn thuốc", code = 400)
        instance.cancelReason = validated_data['cancelReason']
        instance.save()
        return super().update(instance, validated_data)
    def to_representation(self, instance: Prescription):
        return {
            'id': instance.pk,
            'createdAt': instance.createdAt,
            'fromDate': instance.fromDate,
            'toDate': instance.toDate,
            'status': instance.cancelReason,
            'note':  from_json(instance.note) if instance.note else [] 
        }
    
    def to_internal_value(self, data):
        return super().to_internal_value(data)
