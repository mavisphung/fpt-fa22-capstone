from unicodedata import name
from django.urls import path
from treatment import views

urlpatterns = [
    path('contract/', views.CreateContractView.as_view(),name='create_contract'),
    path('contract/supervisor/<int:contract>/<str:action>', views.SupervisorUpdateContractView.as_view(),name='doctor_update_contract_view'),
    path('contract/supervisor/<int:contract>', views.SupervisorTreatmentContractView.as_view(), name='supervisor_contract_detail'),
    path('contract/supervisor/list/', views.SupervisorTreatmentContractListView.as_view(),name='supervisor_list_contract'),
    path('contract/doctor/list/', views.DoctorTreatmentContractListView.as_view(),name='supervisor_list_contract'),
    path('contract/doctor/<int:contract>/', views.DoctorTreatmentContractView.as_view(), name='doctor_contract_detail'),
    path('contract/doctor/<int:contract>/<str:action>/', views.DoctorUpdateContractView.as_view(),name='doctor_update_contract_view'),
    path('contract/test/<int:contract>/', views.TestOrderView.as_view(),name='doctor_order_contract_view'),
    path('contract/doctor/session/', views.DoctorTreatmentSessionCreateView.as_view(),name='doctor_contract_session_view'),
    path('contract/doctor/session/readonly/', views.DoctorTreatmentSessionView.as_view(),name='doctor_contract_read_session_view'),
    path('contract/doctor/cancel/session/', views.DoctorCancelTreatmentSessions.as_view(),name='doctor_contract_cancel_session_view'),
    path('contract/supervisor/session/readonly/<int:contract>/', views.SupervisorTreatmentSessionView.as_view(),name='supervisor_contract_read_session_view'),
    path('contract/supervisor/session/', views.SupervisorCancelTreatmentSessions.as_view(),name='supervisor_contract_cancel_session_view'),
    path('contract/supervisor/session/checkin', views.SupervisorCheckInSessionView.as_view(),name='supervisor_contract_checkin_session_view'),
    path('contract/doctor/session/suggestion', views.SuggestHoursOfDoctorView.as_view(),name='doctor_contract_checkin_session_view'),
]
