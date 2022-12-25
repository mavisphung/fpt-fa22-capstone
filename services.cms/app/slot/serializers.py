from doctor.models import Doctor
from slot.models import DoctorSlot
from rest_framework import serializers

class SlotCreateSerializer(serializers.Serializer):
    date = serializers.DateField()
    start = serializers.TimeField()
    end = serializers.TimeField()
    status = serializers.CharField()

    def create(self, validated_data):
        start = validated_data['start']
        end  = validated_data['end']
        date = validated_data['date']
        doctor:Doctor = self.context['doctor']
        slot = DoctorSlot(start = start, end = end, doctor = doctor, date = date)
        slot.save()
        return slot

class SlotUpdateSerializer(serializers.Serializer):
    status = serializers.CharField()
    
    def update(self, instance:DoctorSlot, validated_data):
        instance.status = validated_data['status']
        return instance

class SupervisorReadonlySerializer(serializers.Serializer):
    status = serializers.CharField()
    def to_representation(self, instance:DoctorSlot):
        return {
            'date': instance.date,
            'start': instance.start,
            'end': instance.end,
        }
