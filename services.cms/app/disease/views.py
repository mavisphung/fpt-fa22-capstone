from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.request import Request
from disease.models import Disease
from shared.utils import get_page_limit_from_request, get_paginated_response
from disease.serializers import DiagnoseSerializer, ReadOnlyDiseaseSerializer
from shared.formatter import format_response
from shared.app_permissions import IsDoctor
from shared.response_messages import ResponseMessage
from shared.exceptions import CustomValidationError
from django.db.models import Q

class DiagnoseView(generics.ListAPIView, generics.CreateAPIView, generics.DestroyAPIView):
    serializer_class = DiagnoseSerializer
    permission_classes = [IsDoctor]

    def create(self, request: Request, *args, **kwargs):
        recordId = request.data['recordId']
        diseaseId = request.data['diseaseId']
        detail = request.data['detail']
        serializer: DiagnoseSerializer = self.get_serializer(
            record=recordId,
            disease=diseaseId,
            description=detail)
        serializer.is_valid(raise_exception = True)
        response = format_response(
            success=True,
            status=200,
            data=serializer.data)
        return Response(response, response['status'])
    
class GetDiseaseView(generics.ListAPIView):
    
    serializer_class = ReadOnlyDiseaseSerializer
    permission_classes = [permissions.AllowAny]
    
    def list(self, request: Request, *args, **kwargs):
        page, limit = get_page_limit_from_request(request)
        if 'code' in request.query_params and 'keyword' in request.query_params:
            raise CustomValidationError(
                message = ResponseMessage.INVALID_INPUT,
                detail = {'params': 'Only contain one "code" or "keyword" param'}
            )
        query = Q()
        code = request.query_params.get('code', '')
        keyword = request.query_params.get('keyword', '')
        if code:
            query.add(Q(otherCode__icontains = code), Q.AND)
        if keyword:
            query.add(Q(vGeneralName__icontains = keyword), Q.AND)
        queryset = Disease.objects.filter(query)
        response = get_paginated_response(queryset, page, limit, self.get_serializer_class())
        
        return response