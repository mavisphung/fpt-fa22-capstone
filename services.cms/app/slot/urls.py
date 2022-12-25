from django.urls import path
from slot import views
urlpatterns = [
    path('doctor/slot', views.AutoCreateSlotAPIView.as_view(), name='create slot view'),
]
