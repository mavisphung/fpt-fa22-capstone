
from django.urls import path
from hello_world import views

urlpatterns = [
    path('', views.HelloWorldView.as_view(), name = 'hello_world'),
    path('cicd/', views.TestCustomView.as_view(), name = 'ci-cd'),
    path('decode-jwt/', views.TokenDecodeView.as_view(), name = 'jwt-decode'),
    path('run-job/', views.RunJobView.as_view(), name = 'scheduled-jobs'),
    path('fetch-distance/', views.GoogleMapAPIView.as_view(), name = 'google-map-api'),
    path('push-notification/', views.PushNotificationAPIView.as_view(), name = 'push-notification'),
    path('async/', views.async_view, name = 'tesseract-ocr'),
    path('image-to-string/', views.TesseractTestView.as_view(), name = 'tesseract-ocr'),
    path('django-async/', views.index),
    path('send-me/', views.SendHealthRecordView.as_view(), name = 'send-health-record'),
]