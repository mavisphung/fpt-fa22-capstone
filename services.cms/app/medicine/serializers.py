from medicine.models import Medicine
from rest_framework import serializers

class ReadOnlyMedicineSerializer(serializers.BaseSerializer):
    
    def to_representation(self, instance: Medicine):
        return {
            'id': instance.pk,
            'name': instance.name,
        }