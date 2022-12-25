from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from django.contrib.auth.models import AnonymousUser

from user.models import User, UserType
import logging
logger = logging.getLogger(__name__)


class IsDoctor(BasePermission):
    
    def has_permission(self, request: Request, view) -> bool:
        user = getattr(request, 'user', None)
        if user is None or isinstance(user, AnonymousUser):
            return False
        
        if user.type == UserType.DOCTOR and user.is_active:
            logger.info(f'{user.email} with {user.type} type performed action')
            return True

        return False
    
class IsSupervisor(BasePermission):
    
    def has_permission(self, request: Request, view) -> bool:
        user = getattr(request, 'user', None)
        if user is None or isinstance(user, AnonymousUser):
            return False
        
        if user.type == UserType.MEMBER and user.is_active:
            logger.info(f'{user.email} with {user.type} type performed action')
            return True

        return False
    
class IsManager(BasePermission):
    
    def has_permission(self, request: Request, view) -> bool:
        user = getattr(request, 'user', None)
        if not user or isinstance(user, AnonymousUser):
            return False
        
        if user.type == UserType.MANAGER and user.is_active:
            logger.info(f'{user.email} with {user.type} type performed action')
            return True
        
        return False