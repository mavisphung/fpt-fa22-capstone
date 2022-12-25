from rest_framework import generics, permissions
from rest_framework.request import Request
from rest_framework.response import Response
from medicine.models import Medicine
from medicine.serializers import ReadOnlyMedicineSerializer
from shared.utils import get_page_limit_from_request, get_paginated_response

# Create your views here.
class ListMedicinesView(generics.ListAPIView):
    
    permission_classes = [permissions.AllowAny]
    serializer_class = ReadOnlyMedicineSerializer
    
    def list(self, request: Request, *args, **kwargs):
        page, limit = get_page_limit_from_request(request)
        keyword = request.query_params['keyword']
        queryset = Medicine.objects.filter(name__icontains = keyword).all()
        return get_paginated_response(queryset, page, limit, self.get_serializer_class())