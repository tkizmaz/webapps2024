from django.urls import path, include

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('staffHome/', views.viewStaffHome, name = 'staffHome'),
    path('users/', views.viewUsers, name= 'viewUsers'),
    path('transactions/', views.viewTransactions, name= 'viewTransactions'),
    path('requests/', views.viewRequests, name= 'viewRequests'),
    path('adminRegister/', views.adminRegister, name= 'adminRegister'),
    path('api/', include('rest_framework.urls'))
]