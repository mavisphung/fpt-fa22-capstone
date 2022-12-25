from django.urls import path
from doctor import views

urlpatterns = [
    # path('', views.HelloWorldView.as_view(), name = 'hello_world')
    path('doctor/register/', views.CreateDoctorView.as_view(), name = 'doctor-registration'),
    path('doctor/<int:pk>/', views.GetDoctorInfoView.as_view(), name = 'get-doctor-info'),
    path('doctor/shifts/', views.ListUpdateDoctorShiftsView.as_view(), name = 'get-doctor-shifts'),
    path('doctors/', views.ListDoctorsView.as_view(), name = 'list-doctors-info'),
    # home screen
    path('doctors/nearest/', views.ListNearestDoctorsView.as_view(), name = 'list-doctors-info-nearest'),
    
    # API for package, duration, package (Legacy)
    path('doctor/<int:pk>/packages/', views.ListCreatePackageView.as_view(), name = 'list-create-packages'),
    path('doctor/<int:doctor_id>/packages/<int:package_id>/', views.RemovePackageView.as_view(), name = 'remove-packages'),
    
    # API For delete shift
    path('doctor/shifts/<int:pk>/', views.RemoveDoctorShiftsView.as_view(), name = 'remove-doctor-shift'),
    
    # API for manager
    path('manager/doctor/register/', views.ManagerCreateDoctorView.as_view(), name = 'manage-create-doctor-api'),
    path('manager/doctor/<int:pk>/lock/', views.LockDoctorView.as_view(), name = 'manage-lock-doctor-api'),
    path('doctor/<int:doctor_id>/services/', views.ListCreateDoctorServiceView.as_view(), name = 'list-create-doctor-services'),
    
    # Service (main)
    # path('doctor/<int:pk>/services/', views.ListCreateDoctorServiceView.as_view(), name = 'list-create-doctor-services'),
    path('doctor/<int:pk>/services/contract/', views.ListServiceContractView.as_view(), name = 'list-contract-services'),
    path('doctor/<int:doctor_id>/services/<int:service_id>/', views.RetrieveUpdateDestroyDSView.as_view(), name = 'remove-services'),

    # Search
    path('api/doctor/search/', views.SearchDoctorView.as_view(), name = 'search-doctor-api'),
    path('api/manager/doctor/search/', views.ManagerSearchDoctorView.as_view(), name = 'manager-search-doctor-api'),
]