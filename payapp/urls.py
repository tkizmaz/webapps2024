from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.viewHome, name = 'home'),
    path('transaction/', views.transferDirectMoney, name= "transaction"),
    path('requestMoney/', views.requestMoney, name= 'requestMoney'),
    path('accountInfo/', views.viewAccountInfo, name= 'accountInfo'),
    path('transactionHistory/', views.viewTransactionHistory, name= 'transactionHistory'),
    path('notifications/', views.viewNotifications, name= 'notifications'),
]