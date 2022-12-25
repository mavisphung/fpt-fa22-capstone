from django.urls import path
from appointment import views
urlpatterns = [
    path('appointments/', views.ListCreateAppointmentView.as_view(),name='create_appointments'),
    path('appointments/<int:pk>/', views.GetAppointmentView.as_view(),name='get_appointment_with_id'),
    path('appointments/doctor/<int:pk>/checkin/', views.CheckInAppointmentView.as_view(),name='check_in_appointments'),
    path('appointments/doctor/<int:pk>/checkout/', views.CheckOutAppointmentView.as_view(),name='check_out_appointments'),
    path('appointments/<int:pk>/reschedule/', views.RescheduleAppointmentView.as_view(),name='reschedule_appointments'),
    path('appointments/<int:pk>/cancel/', views.CancelAppointmentView.as_view(),name='cancel_appointments'),
    # path('appointment/<int:pk>',AcceptAppointmentView.as_view(),name='update_appointments'),
    # path('appointment',ViewAppointment.as_view(), name='view_appointments'),
    path('appointments/doctor/', views.DoctorListAppointmentView.as_view(), name='doctor_view_appointments'),
    path('appointments/doctor/pending/', views.DoctorListPendingAppointmentView.as_view(), name='doctor_view_pending_appointments'),
    
    path('user/me/appointments/', views.ListSheduledAppointmentView.as_view(), name='supervisor_list_appointment'),
    path('user/me/appointments/history/', views.SupervisorListHistoryAppointmentView.as_view(), name='supervisor_list_historical_appointments'),
    
]