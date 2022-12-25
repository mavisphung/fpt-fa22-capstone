from rest_framework import serializers
from specialist.models import Specialist, DoctorSpecialist
from doctor.serializers import ReadOnlyDoctorSerializer

class ReadOnlySpecialistSerializer(serializers.BaseSerializer):
    
    def to_representation(self, instance: Specialist):
        return {
            'id': instance.pk,
            'name': instance.name,
            'description': instance.description,
        }

class ReadOnlyHomeSpecialistSerializer(serializers.BaseSerializer):
    
    def to_representation(self, instance: Specialist):
        if hasattr(instance, 'doctor_list'):
            doctors = ReadOnlyDoctorSerializer(instance.doctor_list, many = True).data
        else:
            doctors = []
        return {
            'id': instance.pk,
            'name': instance.name,
            'description': instance.description,
            'doctors': doctors,
        }
        
class ReadOnlyDoctorSpecialistSerializer(serializers.BaseSerializer):
    
    def to_representation(self, instance: DoctorSpecialist):
        
        return {
            'specialist': instance.specialist_id,
            'doctor': {
                'id': instance.doctor_id,
                'firstName': instance.doctor.firstName,
                'lastName': instance.doctor.lastName,
                'experienceYears': instance.doctor.experienceYears,
                'totalPoints': instance.doctor.totalPoints,
                'turns': instance.doctor.turns,
                'address': instance.doctor.address,
                'avatar': instance.doctor.avatar,
                'gender': instance.doctor.gender
            }
        }