from rest_framework import serializers, exceptions
from shared.utils import check_valid_image_exts

class MetadataSerializer(serializers.Serializer):
    ext = serializers.CharField(max_length = 5)
    size = serializers.FloatField(min_value = 0.0, max_value = 25.0)

class ImageSerializer(serializers.Serializer):
    images = serializers.ListField(
        child = MetadataSerializer(),
        write_only = True,
        allow_empty = False
    )
    
    def validate_images(self, data):
        validated_data = []
        for item in data:
            ext = check_valid_image_exts(item.get('ext'))
            if not ext:
                raise exceptions.ValidationError('Must be an image file')
            validated_data.append(ext)
            
        return validated_data
    