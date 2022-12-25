from rest_framework import serializers

from video_call.models import VideoConference

class ReadOnlyDoctorVideoConferenceSerializer(serializers.Serializer):
    def to_representation(self, instance:VideoConference):
        return {
            'pk': instance.pk,
            'chanel':instance.channel, 
            'token': instance.doctorToken,
            'isExpire': instance.isExpire,
            'beginAvailable': instance.beginAt,
        }

class ReadOnlySupervisorVideoConferenceSerializer(serializers.Serializer):
    def to_representation(self, instance:VideoConference):
        return {
            'pk': instance.pk,
            'chanel':instance.channel, 
            'token': instance.supervisorToken,
            'isExpire': instance.isExpire,
            'beginAvailable': instance.beginAt,
        }

