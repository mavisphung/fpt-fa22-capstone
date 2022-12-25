from rest_framework import generics, status, exceptions, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.request import Request
from user.wallet_serializers import DepositSerializer, WithdrawalSerializer
from shared.models import WeekDay
from shared.response_messages import ResponseMessage
from shared.utils import get_page_limit_from_request, get_random_string, send_html_mail, get_group_by_name
from shared.paginations import get_paginated_response
from shared.formatter import format_response
from user.models import User


class DepositView(generics.CreateAPIView):
    serializer_class = DepositSerializer
    
    def create(self, request: Request, *args, **kwargs):
        account: User = request.user
        serializer: DepositSerializer = self.get_serializer(data = request.data, context = {'account': account})
        serializer.is_valid(raise_exception = True)
        serializer.save()
        
        response = format_response(
            success = True,
            status = 201,
            message = ResponseMessage.WALLET_DEPOSIT_SUCCEEDED,
            data = serializer.data
        )
        
        return Response(response, response['status'])
    
class WithdrawalView(generics.CreateAPIView):
    serializer_class = WithdrawalSerializer
    
    def create(self, request: Request, *args, **kwargs):
        account: User = request.user
        serializer: WithdrawalSerializer = self.get_serializer(data = request.data, context = {'account': account})
        serializer.is_valid(raise_exception = True)
        serializer.save()
        
        response = format_response(
            success = True,
            status = 201,
            message = ResponseMessage.WALLET_WITHDRAW_SUCCEEDED,
            data = serializer.data
        )
        
        return Response(response, response['status'])
