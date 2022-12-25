from rest_framework import serializers
from service.models import Service, DoctorService
from shared.models import ServiceCategory

class ReadOnlyServiceSerializer(serializers.BaseSerializer):
    
    def to_representation(self, instance: Service):
        return {
            'id': instance.pk,
            'name': instance.name,
            'category': instance.category,
            'description': instance.description,
            'method': instance.method,
            'price': instance.price,
        }
        
class ServiceSerializer(serializers.Serializer):
    name = serializers.CharField(max_length = 64)
    description = serializers.CharField(max_length = 500)
    price = serializers.FloatField(min_value = 0.0)
    category = serializers.ChoiceField(choices = ServiceCategory.choices)
    
    def create(self, validated_data: dict):
        service = Service(**validated_data)
        service.save()
        return service
    
    def update(self, instance: Service, validated_data: dict):
        update_fields = ['updatedAt']
        for key, value in validated_data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
                update_fields.append(key)
        instance.save(update_fields = update_fields)
        return instance
    
    def to_representation(self, instance: Service):
        return {
            'id': instance.pk,
            'name': instance.name,
            'category': instance.category,
            'description': instance.description,
            'price': instance.price,
        }
    
    class Meta:
        fields = ['name', 'description', 'price', 'category']