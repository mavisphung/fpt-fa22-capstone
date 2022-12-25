from django.urls import path
from uploads import views

urlpatterns = [
    # path('', views.HelloWorldView.as_view(), name = 'hello_world')
    path('get-presigned-urls/', views.UploadImageView.as_view(), name = 'get-presigned-urls'),
]