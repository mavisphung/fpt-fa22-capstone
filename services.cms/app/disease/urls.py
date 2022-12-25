from django.urls import path
from disease import views

urlpatterns = [
    # path('', views.HelloWorldView.as_view(), name = 'hello_world')
    path('diseases/', views.GetDiseaseView.as_view(), name = 'get-diseases'),
]