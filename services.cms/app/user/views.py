from rest_framework import generics, status, exceptions, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.request import Request
from shared.models import WeekDay
from shared.response_messages import ResponseMessage
from shared.utils import get_page_limit_from_request, get_random_string, send_html_mail, get_group_by_name
from shared.paginations import get_paginated_response
from user.serializers import (
    AuthEmailSerializer, CheckPasswordSerializer, CreateManagerSerializer, 
    DefaultUserSerializer, DeviceSerializer, EmailSerializer, PasswordSerializer, 
    ProfileSerializer, ProfileSerializer2, ReadOnlyNotificationSerializer, RecoveryPasswordSerializer, UserModelSerializer, 
    ChatMemberSerializer
)
from shared.formatter import format_response
from shared.agora.RtcTokenBuilder2 import Role_Publisher, RtcTokenBuilder as RtcTokenBuilder2
from doctor.models import Doctor, WorkingShift
from user.models import User, UserType
from datetime import datetime, timedelta
from django.db import transaction
from django.contrib.auth.models import Group
from user.permissions import IsCustomAdmin
from myapp.settings import AGORA_CONFIG

import logging
logger = logging.getLogger(__name__)

class UserRegistrationView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = DefaultUserSerializer
    def create(self, request, *args, **kwargs):
        logger.info(f'Access /register/ url at {datetime.now()}')
        serializer: DefaultUserSerializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        
        response = format_response(
            success = True,
            status = status.HTTP_201_CREATED,
            message = ResponseMessage.REGISTRATION_SUCCESS,
            data = serializer.data
        )

        return Response(response, response['status'])

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Use to update user profile and view it
    """
    serializer_class = ProfileSerializer2
    def update(self, request: Request, *args, **kwargs):
        instance: User = request.user
        serializer: ProfileSerializer2 = self.get_serializer(instance = instance, data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        
        response = format_response(
            success = True,
            status = status.HTTP_201_CREATED,
            message = ResponseMessage.UPDATE_PROFILE_SUCCESS,
            data = serializer.data
        )

        return Response(response, response['status'])
    
    def retrieve(self, request: Request, *args, **kwargs):
        instance: User = request.user
        serializer: ProfileSerializer2 = self.get_serializer(instance = instance)
        response = format_response(
            success = True,
            status = status.HTTP_200_OK,
            message = ResponseMessage.GET_USER_PROFILE,
            data = serializer.data
        )

        return Response(response, response['status'])
    
class CheckEmailView(generics.CreateAPIView):
    """
    This view checks the email has existed in database or not yet
    """
    serializer_class = EmailSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer: EmailSerializer = self.get_serializer(data = request.data, context = { 'view_name': self.__class__.__name__ })
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data.get('email', None)
        response = format_response(
            success = True,
            status = 201,
            message = ResponseMessage.CHECK_EMAIL_SUCCEEDED if isinstance(user, User) else ResponseMessage.VERIFY_EMAIL_SUCCEEDED
        )
        
        return Response(response, response['status'])
    
class ActivateAccountView(generics.CreateAPIView):
    
    serializer_class = EmailSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        logger.info('ActivateAccount is invoked')
        serializer: EmailSerializer = self.get_serializer(data = request.data, context = { 'view_name': self.__class__.__name__ })
        serializer.is_valid(raise_exception = True)

        response = format_response(
            success = True,
            status = 201,
            message = ResponseMessage.UPDATE_STATUS_ACCOUNT
        )
        
        return Response(response, response['status'])
    
class ResendVerificationCodeView(generics.CreateAPIView):

    serializer_class = EmailSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        logger.info('Resend verification code invoked')
        serializer: EmailSerializer = self.get_serializer(data = request.data, context = { 'view_name': self.__class__.__name__ })
        serializer.is_valid(raise_exception = True)
        
        response = format_response(
            success = True,
            status = 201,
            message = ResponseMessage.SEND_MAIL_SUCCEEDED
        )
        
        return Response(response, response['status'])
    
class ChangePasswordView(generics.UpdateAPIView):
    
    serializer_class = PasswordSerializer
    
    def update(self, request, *args, **kwargs):
        user: User = request.user
        serializer: PasswordSerializer = self.get_serializer(
            instance = user, 
            data = request.data, 
            context = {'user': user}
        )
        serializer.is_valid(raise_exception = True)
        serializer.save()
        
        response = format_response(
            success = True,
            status = 201,
            message = ResponseMessage.PASSWORD_CHANGED_SUCCEEDED
        )
        return Response(response, response['status'])
    
class CheckPasswordView(generics.CreateAPIView):
    
    serializer_class = CheckPasswordSerializer
    
    def create(self, request, *args, **kwargs):
        serializer: CheckPasswordSerializer = self.get_serializer(data = request.data, context = {'user': request.user})
        serializer.is_valid(raise_exception = True)
        
        response = format_response(
            success = True,
            status = 200,
            message = ResponseMessage.PASSWORD_MATCHED
        )
        return Response(response, response['status'])
    
class CheckAuthenticatedEmailView(generics.UpdateAPIView):
    """
    This view checks the email has existed in database or not yet
    """
    serializer_class = AuthEmailSerializer
    
    def update(self, request, *args, **kwargs):
        serializer: AuthEmailSerializer = self.get_serializer(data = request.data, context = { 'user': request.user })
        serializer.is_valid(raise_exception = True)

        response = format_response(
            success = True,
            status = 201,
            message = ResponseMessage.EMAIL_VALID,
            data = serializer.validated_data
        )
        
        return Response(response, response['status'])
    
class VerifyDoctorAdminView(generics.UpdateAPIView):
    serializer_class = None
    # queryset = Doctor.objects.filter(isApproved = False)
    queryset = Doctor.objects.all()
    
    permission_classes = [IsCustomAdmin]
    
    def _create_shifts(self, doctor: Doctor):
        shifts = []
        for weekday in WeekDay.values:
            shift = WorkingShift(weekday = weekday, doctor = doctor)
            shifts.append(shift)
            
        WorkingShift.objects.bulk_create(shifts)
        logger.info(f'Created 7 shifts for doctor {doctor.pk}')
    
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        # user: User = request.user
        update_fields = ['updatedAt', 'isApproved']
        # Must create API for doctor create account first then implement this
        doctor: Doctor = self.get_object()
        if not doctor.isApproved:
            doctor_group = get_group_by_name(UserType.DOCTOR)
            doctor.isApproved = True
            doctor.save(update_fields = update_fields)
            self._create_shifts(doctor)
            # Process create account for doctor if doctor is approved
            doctor_account = User(
                email = doctor.email,
                firstName = doctor.firstName,
                lastName = doctor.lastName,
                dob = doctor.dob,
                avatar = doctor.avatar,
                age = doctor.age,
                phoneNumber = doctor.phoneNumber,
                address = doctor.address,
                gender = doctor.gender,
                doctor = doctor,
                type = UserType.DOCTOR
            )
            # password = get_random_string(8)
            password = '123456' # bypass for doctor
            doctor_account.set_password(password)
            doctor_account.save()
            doctor_group.user_set.add(doctor_account)
            send_html_mail(
                subject = 'Password for doctor to login',
                body = f'Your password is: {password}',
                to = [doctor_account.email]
            )
            logger.info(f'Doctor email {doctor_account.email} created succeeded!')
        response = format_response(
            success = True,
            status = 202,
            message = ResponseMessage.DOCTOR_APPROVED_BY_ADMIN
        )
        
        return Response(response, response['status'])

class CreateManagerView(generics.CreateAPIView):
    permission_classes = [IsCustomAdmin]
    serializer_class = CreateManagerSerializer
    
    def create(self, request: Request, *args, **kwargs):
        
        serializer: CreateManagerSerializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        
        response = format_response(
            success = True,
            status = 201,
            message = ResponseMessage.REGISTRATION_SUCCESS,
            data = serializer.data
        )
        
        return Response(response, response['status'])

class SendVerificationCodeView(generics.CreateAPIView):
    serializer_class = EmailSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer: EmailSerializer = self.get_serializer(data = request.data, context = { 'view_name': self.__class__.__name__ })
        serializer.is_valid(raise_exception = True)
        
        response = format_response(
            success = True,
            status = 201,
            message = ResponseMessage.VERIFY_CODE_SENT
        )
        
        return Response(response, response['status'])

class RecoveryPasswordView(generics.UpdateAPIView):
    
    permission_classes = [permissions.AllowAny]
    serializer_class = RecoveryPasswordSerializer
    
    def update(self, request, *args, **kwargs):
        serializer: RecoveryPasswordSerializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        
        return Response(status = status.HTTP_204_NO_CONTENT)
    
class GetUserView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserModelSerializer

    def list(self, request: Request, *args, **kwargs):
        page: int = int(request.query_params.get('page', 1))
        limit: int = int(request.query_params.get('limit', 10))
        
        queryset = User.objects.all()
        response = get_paginated_response(ret_list = queryset, page_number = page, limit = limit, serializer_class = self.get_serializer_class())

        return response
    
class DeviceRegistrationView(generics.CreateAPIView):
    
    serializer_class = DeviceSerializer
    permission_classes = [ permissions.AllowAny ]
    
    def create(self, request: Response, *args, **kwargs):
        serializer: DeviceSerializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        
        serializer.save()
        response = format_response(
            success = True,
            status = 201,
            message = ResponseMessage.DEVICE_REGISTER_SUCCEEDED,
            data = serializer.data
        )
        return Response(response, response['status'])
    

@api_view(['GET'])
def get_agora_token(request: Request):
    # channel_name = "chanel1"
    # uid = 1234121235
    # account = ""
    user: User = request.user
    # channel_name = get_random_string()
    channel_name = 'aaa'
    # uid = user.pk
    uid = 0
    # uid = user.email
    # account = 0
    
    vietnamese_time = datetime.now() + timedelta(hours = 7)
    expired_time_in_second = vietnamese_time.timestamp() + AGORA_CONFIG.get('token_expiration_in_seconds', 3600)
    privilege_expiration_in_seconds = vietnamese_time.timestamp() + AGORA_CONFIG.get('privilege_expiration_in_seconds', 3600)
    
    token = RtcTokenBuilder2.build_token_with_uid(
        AGORA_CONFIG.get('app_id'),
        AGORA_CONFIG.get('app_certificate'), 
        channel_name, 
        uid,
        Role_Publisher, 
        expired_time_in_second,
        privilege_expiration_in_seconds
    )
    
    response = format_response(
        success = True,
        status = 200,
        message = ResponseMessage.AGORA_TOKEN_OBTAINED,
        data = { 
            'token': token,
            'channel': channel_name,
            'uid': uid,
            # 'token_live': token_live,
        }
    )
    
    return Response(response, response['status'], content_type = 'application/json')

class GetNotificationView(generics.ListAPIView):
    
    serializer_class = ReadOnlyNotificationSerializer
    
    def list(self, request: Request, *args, **kwargs):
        user: User = request.user
        page, limit = get_page_limit_from_request(request)
        
        queryset = user.notifications.order_by('-createdAt').all()

        return get_paginated_response(queryset, page, limit, self.get_serializer_class())


class GetChatInfo(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    
    def retrieve(self, request:Request, *args, **kwargs):
        
        user:User = request.user
        userId = request.query_params['userId']
        guest:User = User.objects.filter(pk = userId).first()
        if guest is None:
            return Response(data = {}, status = 404)      
        serializer = ChatMemberSerializer(guest)
        response = format_response(data = serializer.data, status = 200)
        print(serializer.data)
        return Response(data = response['data'], status = 200)
        