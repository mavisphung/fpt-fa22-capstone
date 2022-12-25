from django.urls import path
from transaction import views
urlpatterns = [
    path('ipn', views.CreateTransactionIPNView.as_view(), name='ipn_view'),
    path('ipn', views.CreateTransactionView.as_view(), name='add_balance')
]
