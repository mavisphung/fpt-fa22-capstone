from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.response import Response
from django.template.exceptions import TemplateDoesNotExist, TemplateSyntaxError
from shared.formatter import format_response
from .response_messages import ResponseMessage
import logging
logger = logging.getLogger(__name__)

def __handle_APIException(exc: Response, context, response = None):
    response = format_response(
        success = False,
        status = 500,
        message = ResponseMessage.INTERNAL_SERVER_ERROR,
        data = exc.data
    )
    return Response(response, response['status'], headers = exc.headers)

def __handle_type_error(exc, context, response = None):
    response = format_response(
        success = False,
        status = exc.status_code if hasattr(exc, 'status_code') else status.HTTP_500_INTERNAL_SERVER_ERROR,
        message = ResponseMessage.NO_TYPE_ERROR,
        data = exc.args
    )
    return Response(response, response['status'])

def __handle_validation_error(exc, context, response = None):
    # print('type(exc)', type(exc))
    # print('dir(exc)', dir(exc))
    response = format_response(
        success = False,
        status = 400,
        message = ResponseMessage.INVALID_INPUT,
        data = exc.detail
    )
    return Response(response, response['status'])

def __handle_key_error(exc, context, response = None):
    response = format_response(
        success = False,
        status = 500,
        message = ResponseMessage.NO_KEY_ERROR,
        data = exc.args
    )
    return Response(response, response['status'])

def __handle_authentication_failed(exc, context, response = None):
    response = format_response(
        success = False,
        status = 401,
        message = ResponseMessage.AUTHENTICATION_FAILED,
        data = exc.detail
    )
    return Response(response, response['status'])

def __handle_not_authenticated(exc, context, response = None):
    response = format_response(
        success = False,
        status = 401,
        message = ResponseMessage.NO_CREDENTIALS_PROVIDED,
        data = exc.detail
    )
    return Response(response, response['status'])

def __handle_invalid_token(exc, context, response = None):
    response = format_response(
        success = False,
        status = 401,
        message = ResponseMessage.INVALID_TOKEN,
        data = exc.detail
    )
    return Response(response, response['status'])

def __handle_permissions_denied(exc, context, response = None):
    response = format_response(
        success = False,
        status = 403,
        message = ResponseMessage.PERMISSION_DENIED,
        data = exc.detail
    )
        
    return Response(response, response['status'])

def __handle_not_active_user(exc, context, response = None):
    response = format_response(
        success = False,
        status = 401,
        message = ResponseMessage.INACTIVE_USER
    )
    return Response(response, response['status'])

def __handle_custom_validation_error(exc, context, response = None):
    # print(dir(exc))
    response = format_response(
        success = False,
        status = 400,
        message = exc.message,
        data = exc.detail if hasattr(exc, 'detail') else {}
    )
    return Response(response, response['status'])

def __handle_parse_error(exc, context, response = None):
    response = format_response(
        success = False,
        status = 400,
        message = exc.detail
    )
    return Response(response, response['status'])

def __handle_http404(exc, context, response = None):
    logger.error(str(exc))
    print(exc.args)
    response = format_response(
        success = False,
        status = 404,
        message = ResponseMessage.NOT_FOUND
    )
    return Response(response, response['status'])

def __handle_attribute_error(exc: AttributeError, context, response = None):
    logger.error(str(exc))
    response = format_response(
        success = False,
        status = 500,
        message = ResponseMessage.NO_ATTRIBUTE_ERROR,
        data = exc.args
    )
    return Response(response, response['status'])

def __handle_template_error(exc: TemplateDoesNotExist, context, response = None):
    logger.error(str(exc))
    response = format_response(
        success = False,
        status = 500,
        message = ResponseMessage.TEMPLATE_NOT_EXISTED,
        data = exc.args
    )
    return Response(response, response['status'])
    
cached_exceptions = {
    # 'APIException': __handle_APIException,
    'TypeError': __handle_type_error,
    'ValidationError': __handle_validation_error,
    'KeyError': __handle_key_error,
    'AuthenticationFailed': __handle_authentication_failed,
    'PermissionDenied': __handle_permissions_denied,
    'NotAuthenticated': __handle_not_authenticated,
    'InvalidToken': __handle_invalid_token,
    'NotActiveUserException': __handle_not_active_user,
    'CustomValidationError': __handle_custom_validation_error,
    'ParseError': __handle_parse_error,
    'SocialLoginException': __handle_custom_validation_error,
    'Http404': __handle_http404,
    'AttributeError': __handle_attribute_error,
    'DoesNotExist': __handle_http404,
    'TemplateDoesNotExist': __handle_template_error,
}

def custom_exception_handler(exc, context):
    
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    # exception = exception_handler(exc, context)
    # Now add the HTTP status code to the response.
    # if exception is not None:
    #     response = format_response(
    #         success = False,
    #         status = exception.status_code if exception else status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         message = exception.status_text,
    #         data = exception.data
    #     )
    #     return Response(response, response.get('status'))
    
    exception_name = exc.__class__.__name__
    logger.info(exception_name)
    logger.info(exc.args)
    if exception_name in cached_exceptions:
        return cached_exceptions[exception_name](exc, context)
    
    response = format_response(
        success = False,
        status = 500,
        message = ResponseMessage.INTERNAL_SERVER_ERROR,
        data = exc.detail if hasattr(exc, 'detail') else {'errors': exc.args}
    )
    
    return Response(response, response.get('status'))


