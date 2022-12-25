from django.urls import path
from schedule import views

urlpatterns = [
    path('schedule/', views.AvailableSlotView.as_view(), name='doctor_schedule'),
    # API for checking data
    path('api/suggest/doctor/<int:doctor_id>/', views.SuggestHoursOfDoctorView.as_view(), name='suggest-doctor-hour'),
]
