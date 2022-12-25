"""myapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView
# )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('hello_world.urls')),
    path('', include('user.urls')),
    # path('login/', TokenObtainPairView.as_view(), name = 'token-verify'),
    path('', include('auth.urls')),
    path('', include('uploads.urls')),
    path('', include('doctor.urls')),
    path('', include('patient.urls')),
    path('', include('health_record.urls')),
    path('', include('appointment.urls')),
    path('', include('schedule.urls')),
    path('', include('prescription.urls')),
    path('', include('instruction.urls')),
    path('', include('specialist.urls')),
    path('', include('disease.urls')),
    path('', include('medicine.urls')),
    path('', include('treatment.urls')),
    path('', include('transaction.urls')),
    path('', include('service.urls')),
    path('', include('slot.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)