from django.contrib.auth.models import Group
from shared.response_messages import ResponseMessage
from user.models import Notification, User, VerificationCode
from shared.models import Gender, WeekDay
from rest_framework import exceptions
from rest_framework.request import Request
from django.core.mail.message import EmailMessage
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.utils import timezone
from rest_framework.response import Response
from shared.exceptions import CustomValidationError
from datetime import datetime, time, timedelta
from django.db import transaction

from myapp import settings
import threading, string, random, os, re, json

import logging
logger = logging.getLogger(__name__)

EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def check_valid_email(email: str) -> bool:
    if re.fullmatch(EMAIL_REGEX, email):
        return True
    return False

def get_group_by_name(group_name) -> Group:
    """Return Group object. If not, raise ValidationError"""
    try:
        return Group.objects.get(name = group_name)
    except Group.DoesNotExist:
        raise exceptions.ValidationError({'group': f'The group {group_name} does not exist'})

def get_user_by_email(email) -> User:
    """
    Return User object. If not, raise ValidationError
    """
    try:
        return User.objects.get(email = email)
    except User.DoesNotExist:
        raise exceptions.ValidationError({'user': f'{email} does not exist'})

def get_random_string(size=6, chars=string.ascii_uppercase + string.digits) -> str:
    return ''.join(random.choice(chars) for _ in range(size))

def generate_verify_code(user: User) -> VerificationCode:
    code = VerificationCode(
        # code = get_random_string(chars = string.digits),
        code = '123456', # For mobile dev bypass
        expiredAt = timezone.now() + timezone.timedelta(minutes = settings.EXPIRY_TIME_IN_MINUTES),
        user = user
    )
    code.save()
    return code

IMAGE_EXTS = {
    'png': 'png',
    'jpg': 'jpg',
    'jpeg': 'jpeg',
    'svg': 'svg'
}
def check_valid_image_exts(ext):
    if ext in IMAGE_EXTS:
        return ext
    return None

def get_paginated_data(
    success: bool = False, 
    statusCode = None, 
    message: str = None,
    totalItems: int = 0,
    nextPage: int = None,
    previousPage: int = None,
    currentPage: int = 0,
    totalPages: int = 0,
    limit: int = 10,
    data = None
):
    return {
        'success': success,
        'statusCode': statusCode,
        'message': message,
        'totalItems': totalItems,
        'nextPage': nextPage,
        'previousPage': previousPage,
        'currentPage': currentPage,
        'totalPages': totalPages,
        'limit': limit,
        'data': data if isinstance(data, dict) or isinstance(data, list) else []
    }

def get_paginated_response(ret_list, page_number, limit, serializer_class = None) -> Response:
    print('before error paging')    
    paginator = Paginator(ret_list, limit) # new one Paginator instance
    page = paginator.get_page(page_number) # get page
    if serializer_class:
        serializer = serializer_class(page, many = True) # serialize page
    response = get_paginated_data(
        success = True,
        statusCode = 200,
        message = ResponseMessage.GET_DATA_SUCCEEDED,
        limit = paginator.per_page,
        totalItems = paginator.count,
        totalPages = paginator.num_pages,
        currentPage = page_number,
        nextPage = page_number + 1 if page.has_next() else None,
        previousPage = page_number - 1 if page.has_previous() else None,
        data = serializer.data if serializer_class else page.object_list
    )
    return Response(response, response.get('statusCode'))

class EmailThread(threading.Thread):
    def __init__(self, subject, body, to):
        self.subject = subject
        self.body = body
        self.to = to
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMessage(
            subject=self.subject, 
            body=self.body, 
            from_email=os.environ.get('EMAIL_HOST_USER') or 'huypc2410@gmail.com', 
            to=self.to,
        )
        msg.content_subtype = "html"
        msg.send(fail_silently=False)
        
def send_html_mail(subject, to, template: str = None, context: dict = None):
    msg_html = render_to_string(template, context = context)
    try:
        EmailThread(subject, msg_html, to).start()
    except Exception as ex:
        logger.error(f'EmailThread error: {str(ex)}')
        raise exceptions.APIException({'error': ex.args})
    
def get_mail_body(user: User, code: VerificationCode):
    return f"""
        <!DOCTYPE html>
        <html>
        <head>
        <title>
        </title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
        body {{background-color:#ffffff;background-repeat:no-repeat;background-position:top left;background-attachment:fixed;}}
        h4{{font-family:Times, serif;color:#000000;background-color:#ffffff;}}
        p {{font-family:Arial, sans-serif;font-size:14px;font-style:normal;font-weight:normal;color:#000000;background-color:#ffffff;}}
        </style>
        </head>
        <body>
        <h3>Thank you for your registration</h3>
        <p>Dear {"Mr." if user.gender == Gender.MALE else "Mrs."} {user.firstName},</p>
        <p></p>
        <p>We appreciated you to use and trust in our service.</p>
        <p>NOTE: The code is expired after <strong>5 minutes</strong>.</p>
        <p>Your verification code is: {code.code}</p>
        <p></p>
        <p>Regardless,</p>
        <p>Cứu Bé Team</p>
        <p></p>
        <p></p>
        </body>
        </html>
        """
        
def get_resend_body(user: User, code: VerificationCode):
    return f"""
        <!DOCTYPE html>
        <html>
        <head>
        <title>
        </title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
        body {{background-color:#ffffff;background-repeat:no-repeat;background-position:top left;background-attachment:fixed;}}
        h4{{font-family:Times, serif;color:#000000;background-color:#ffffff;}}
        p {{font-family:Arial, sans-serif;font-size:14px;font-style:normal;font-weight:normal;color:#000000;background-color:#ffffff;}}
        </style>
        </head>
        <body>
        <h3>Resend verification code</h3>
        <p>Dear {"Mr." if user.gender == Gender.MALE else "Mrs."} {user.firstName},</p>
        <p></p>
        <p>We appreciated you to use and trust in our service again.</p>
        <p>NOTE: The code is expired after <strong>5 minutes</strong>.</p>
        <p>Your verification code is: {code.code}</p>
        <p></p>
        <p>Regardless,</p>
        <p>Cứu Bé Team</p>
        <p></p>
        <p></p>
        </body>
        </html>
        """

def get_send_code_body(user: User, code: VerificationCode):
    return f"""
        <!DOCTYPE html>
        <html>
        <head>
        <title>
        </title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
        body {{background-color:#ffffff;background-repeat:no-repeat;background-position:top left;background-attachment:fixed;}}
        h4{{font-family:Times, serif;color:#000000;background-color:#ffffff;}}
        p {{font-family:Arial, sans-serif;font-size:14px;font-style:normal;font-weight:normal;color:#000000;background-color:#ffffff;}}
        </style>
        </head>
        <body>
        <h3>Recovery password</h3>
        <p>Dear {"Mr." if user.gender == Gender.MALE else "Mrs."} {user.firstName},</p>
        <p></p>
        <p>We appreciated you to use and trust in our service.</p>
        <p>Then, please note down your password in somewhere in case you forget again.</p>
        <p>NOTE: The code is expired after <strong>5 minutes</strong>.</p>
        <p>Your verification code is: {code.code}</p>
        <p></p>
        <p>Regardless,</p>
        <p>Cứu Bé Team</p>
        <p></p>
        <p></p>
        </body>
        </html>
        """
        
def get_page_limit_from_request(request: Request):
    """
    Return a tuple containing page number, limit
    """
    try:
        page: int = int(request.query_params.get('page', 1))
        limit: int = int(request.query_params.get('limit', 10))
    except:
        page = 1
        limit = 10
    return page, limit


WEEK_DAYS = {
    0: WeekDay.MONDAY,
    1: WeekDay.TUESDAY,
    2: WeekDay.WEDNESDAY,
    3: WeekDay.THURSDAY,
    4: WeekDay.FRIDAY,
    5: WeekDay.SATURDAY,
    6: WeekDay.SUNDAY
}

def convert_weekday(date: datetime) -> WeekDay:
    return WEEK_DAYS[date.weekday()] 

def dict_group_by(data: list, field: str) -> dict:
    ret_data = {}
    for item in data:
        value = item.get(field)
        if value not in ret_data:
            ret_data[value] = []
        ret_data[value].append(item)
    return ret_data

def from_json(data: str) -> dict:
    return json.loads(data)

def to_json(data: dict) -> str:
    return json.dumps(data)

def time_in_range(start, end, x) -> bool:
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end
    
    
# importing googlemaps module
import googlemaps, requests
from myapp.settings import GOOGLE_MAP_API_KEY

# Requires API key
gmaps = googlemaps.Client(key = GOOGLE_MAP_API_KEY)

logger.info('Map API Loaded')

def get_locations(origin, destination_list: list):
    destinations = '|'.join(destination_list)
    locations = gmaps.distance_matrix(origin, destinations)
    # base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
    # response = requests.get(
    #     base_url,
    #     params = {
    #         'origins': origin,
    #         'destinations': destinations,
    #         'key': GOOGLE_MAP_API_KEY
    #     }
    # )
    # locations: dict = response.json()
    if 'error_message' in locations:
        raise CustomValidationError(
            message = 'Google API Error',
            detail = locations
        )
    rows: list = locations.get('rows')
    if rows is None or rows.__len__() == 0:
        return {
            'error': 'Can not fetch data from google api'
        }
    elements = locations['rows'][0]['elements']
    origin_addresses = locations['origin_addresses'][0]
    dest_addresses = locations['destination_addresses']
    data = []
    for el in elements:
        temp = {}
        for key, value in el.items():
            temp[key] = value
        data.append(temp)
    
    return {
        'destination_addresses': dest_addresses,
        'origin_addresses': origin_addresses,
        'locations': data
    }
    
def ceil_dt(dt, delta = timedelta(minutes = 1)) -> datetime:
    return dt + (timezone.make_aware(datetime.min) - dt) % delta

def time_to_int(date: datetime):
    return int(date.strftime('%H%M'))

from django.db import connection
from django.db import reset_queries

def database_debug(func):
    def inner_func(*args, **kwargs):
        reset_queries()
        results = func(*args, **kwargs)
        query_info = connection.queries
        print('function_name: {}'.format(func.__name__))
        print('query_count: {}'.format(len(query_info)))
        queries = ['---{}\n'.format(query['sql']) for query in query_info]
        print('queries: \n{}'.format(''.join(queries)))
        return results
    return inner_func