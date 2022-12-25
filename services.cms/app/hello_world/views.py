from rest_framework import generics, status, exceptions, permissions
from rest_framework.response import Response
from rest_framework.request import Request
from disease.models import Disease
from shared.agora.RtcTokenBuilder2 import Role_Subscriber, RtcTokenBuilder
from health_record.models import HealthRecord
from appointment.serializers import ReadOnlyAppointmentSerializer
from hello_world.serializers import Serializer
from shared.formatter import format_response
from appointment.models import Appointment
from shared.utils import get_locations, get_paginated_response, send_html_mail, gmaps, to_json
from django.template.loader import render_to_string
from django.utils import timezone
from django.http import JsonResponse
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from asgiref.sync import sync_to_async
from rest_framework.decorators import api_view, permission_classes
from myapp import settings
from prescription.models import Prescription, PrescriptionDetail
import asyncio

import jwt, datetime, asyncio
import logging
logger = logging.getLogger(__name__)

class HelloWorldView(generics.ListCreateAPIView, 
                    generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = Serializer
        
    def list(self, request, *args, **kwargs):
        response = format_response(
            success = True, 
            status = status.HTTP_200_OK,
            message = 'Hello world from Django Rest Framework Version 2',
            data = {
                'message': 'This is dataaaaaa'
            }
        )
        logger.info('HelloWorld view just run')
        return Response(response, response.get('status'))

    def create(self, request, *args, **kwargs):
        logger.info('Create view just run hahah')
        raise exceptions.APIException(detail = 'Testing Error')
    
class TestCustomView(generics.RetrieveAPIView):
    
    def retrieve(self, request, *args, **kwargs):
        # msg_html = render_to_string('welcome_email_template.html', {'title': 'Hello world from Django Rest Framework Version', 'verify_code': '123456'})
        # send_html_mail('This is test subject', ['nguoibimatthegioi@gmail.com'], msg_html)
        response = format_response(
            success = True, 
            status = status.HTTP_200_OK,
            message = 'Verify that CI/CD success',
            data = {
                'message': 'This is dataaaaaa'
            }
        )
        return Response(response, response.get('status'))
    
class TokenDecodeView(generics.RetrieveAPIView):
    
    def retrieve(self, request, *args, **kwargs):
        auth = request.auth
        data = jwt.decode(str(auth), settings.SECRET_KEY, algorithms=['HS256'])
        return Response(data)
    
class RunJobView(generics.ListCreateAPIView):
    
    permission_classes = [permissions.AllowAny]
    
    def do_something(self, a, b, c):
        print('pass arguments here')
        print('a =', a)
        print('b =', b)
        print('c =', c)
        
    
    def list(self, request: Request, *args, **kwargs):
        scheduler = BackgroundScheduler()
        a = request.query_params['a']
        b = request.query_params['b']
        c = request.query_params['c']
        now = datetime.datetime.now()
        finish_day = now + datetime.timedelta(seconds = 3)
        date_trigger = DateTrigger(run_date = finish_day)
        # print('----------------- scheduler.print_jobs() -----------------')
        scheduler.add_job(self.do_something, date_trigger, args = (a, b, c), replace_existing = True, id = '123')
        # print(scheduler.print_jobs())
        scheduler.start()
        
        return Response({'message': 'Run job succeeded'})
    
class GoogleMapAPIView(generics.ListAPIView):
    
    permission_classes = [permissions.AllowAny]
    
    def do_something(self, a, b, c):
        print('pass arguments here')
        print('a =', a)
        print('b =', b)
        print('c =', c)
        
    
    def list(self, request: Request, *args, **kwargs):
        base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
        home = '126 Gia Phú, Quận 6'
        destinations_list = ['218/25 Hồng Bàng, Phường 12, Quận 5, TP.HCM', '126 Hồng Bàng, Phường 12, Quận 5, Thành phố Hồ Chí Minh, Việt Nam']
        
        locations = get_locations(home, destinations_list)
        
        return Response({'message': 'get data from google map api succeeded', 'data': locations})
    
class PushNotificationAPIView(generics.ListAPIView):
    
    permission_classes = [permissions.AllowAny]
    
    def list(self, request: Request, *args, **kwargs):
        from firebase_admin.messaging import Message, Notification
        from fcm_django.models import FCMDevice
        devices: FCMDevice = FCMDevice.objects.filter(user_id = 13)
        print(devices)
        # for device in devices:
        # device.send_message(Message(notification=Notification(title="Django app", body="Xin chào tôi là thông báo đến từ django")))
        devices.send_message(
            Message(
                notification = Notification(title="Django app", body="Xin chao chung toi la Cuu Be Team"),
                data = {
                    'id': 'asfasf',
                    'payload': to_json({
                        'arr': ['asd', 'name', 'asdgs'],
                    }),
                }
            )
        )
        return Response()

class TesseractTestView(generics.CreateAPIView):
    
    from rest_framework import parsers
    permission_classes = [permissions.AllowAny]
    parser_classes = [parsers.MultiPartParser, parsers.FileUploadParser]
    
    def create(self, request: Request, *args, **kwargs):
        from pytesseract import pytesseract, Output
        from PIL import Image
        file_obj = request.data['file']
        print(file_obj)
        print(type(file_obj))
        print(pytesseract.get_languages())
        img = Image.open(file_obj)
        text: str = pytesseract.image_to_string(img, lang = 'vie', output_type = Output.STRING, config = settings.TESSDATA_CONFIG)
        return Response({'data': text})

@sync_to_async
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def async_view(request: Request):
    app_id = "2379244a079c45098b6d9040bb37aa85"
    app_certificate = "e65713f9be08465293657ce6efaed640"
    channel_name = "chanel1"
    uid = 1234121235
    account = ""
    token_expiration_in_seconds = 3600
    privilege_expiration_in_seconds = 3600
    
    token = RtcTokenBuilder.build_token_with_user_account(app_id, app_certificate, channel_name, account,
                                                          Role_Subscriber, token_expiration_in_seconds,
                                                          privilege_expiration_in_seconds)
    print("Token with user account: {}".format(token))
    
    
    
    search = Disease.objects.filter(code__icontains = 'A')
    print(search.count())
    print(search)
    list_appointment = Appointment.objects.select_related('patient', 'doctor', 'booker', 'package').all()
    
    return get_paginated_response(
        ret_list = list_appointment,
        page_number = 1,
        limit = 20,
        serializer_class = ReadOnlyAppointmentSerializer
    )
    
from django.http import JsonResponse, HttpRequest

# @permission_classes([permissions.AllowAny])
# @api_view(['GET'])
async def index(request):
    print(type(request))
    print(request)
    # await asyncio.sleep(2)
    
    return JsonResponse({'msg': 'hello world'})

class SendHealthRecordView(generics.CreateAPIView):
    
    permission_classes = [permissions.AllowAny]
    
    def create(self, request: Request, *args, **kwargs):
        receiver = request.data['receiver']
        
        subject = '[HiDoctor] Đơn thuốc đã được tạo'
        to = [receiver]
        send_html_mail(subject, to, 'send_health_record.html', context = {
            'health_record': {
                'id': 10
            },
            'diagnoses': 'aaaaaa',
            'medicalInstructions': 'Chào cơn mưa',
            'prescriptions': ['Hello world', 'Xin chao viet nam', 'Bonjour']
        })
        return Response()