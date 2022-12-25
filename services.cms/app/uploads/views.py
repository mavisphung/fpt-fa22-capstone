from rest_framework import generics, exceptions, permissions
from rest_framework.response import Response
from boto3 import exceptions as boto3_exc
from uploads.serializers import ImageSerializer
from shared.utils import get_random_string
from shared.formatter import format_response
from shared.response_messages import ResponseMessage
from uploads.s3 import S3
from datetime import datetime
from django.utils import timezone
import logging
logger = logging.getLogger(__name__)

class UploadImageView(generics.CreateAPIView):
    
    serializer_class = ImageSerializer
    permission_classes = [permissions.AllowAny]
    def create(self, request, *args, **kwargs):
        """
        Return presigned urls
        """
        logger.info('Prepare to get presigned urls from S3')
        serializer: ImageSerializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        images = serializer.validated_data.get('images')
        s3_client = S3()
        urls = []
        now = datetime.utcnow()
        for ext in images:
            path = '{}/{}/{}/{}.{}'.format(f'{now.year}',f'{now.month}', f'{now.day}', f'{get_random_string()}', ext)
            print('path', path, type(path))
            logger.info('Generate path succeeded')
            presigned_url = s3_client.get_presigned_url(path, 900)
            logger.info('Get full presigned url succeeded')
            urls.append(presigned_url)
        
        response = format_response(
            success = True,
            status = 201,
            message = ResponseMessage.GET_PRESIGNED_URLS,
            data = {'urls': urls}
        )
        
        return Response(response, status = response['status'])