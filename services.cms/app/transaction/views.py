from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from shared.exceptions import CustomValidationError
from myapp.settings import VNPAY_CONFIG
from transaction.models import Order
from transaction.serializers import CTransactionSerializer, VnPayCreateTransactionSerializer
import hmac
import json
from transaction.util import vnpay
from collections import OrderedDict
from shared.formatter import format_response

class CreateTransactionIPNView(generics.ListAPIView):
    serializer_class = VnPayCreateTransactionSerializer
    def list(self, request:Request, *args, **kwargs):
        vnp = vnpay()
        vn_params = request.query_params.copy()
        for key, value in vn_params.items():
            vnp.requestData[key] = value
        is_valid  = vnp.validate_response(VNPAY_CONFIG['vnp_HashSecret'])
        if is_valid:
            vnp.get_payment_url()
            
        return Response(data = vnp.responseData, status = 200)

class CreateTransactionView(generics.CreateAPIView):
    serializer_class = CTransactionSerializer
    def create(self, request: Request, *args, **kwargs):
        serializer: CTransactionSerializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception= True)
        serializer.save()
        reposne = format_response(success= True, message='Nạp tiền vào tài khoản thành công', data = serializer.data)
        return Response(data = reposne['data'], status = reposne['status'])
    