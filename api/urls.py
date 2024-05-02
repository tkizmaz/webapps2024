from django.urls import path
from . import views

urlpatterns = [
    path('conversion/<str:senderCurrency>/<str:receiverCurrency>/<str:amount>/', views.convertCurrency, name='convertCurrency'),
]
