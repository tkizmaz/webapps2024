from rest_framework import generics
from payapp.models import Transaction
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponseNotFound

def convertCurrency(request, senderCurrency, receiverCurrency, amount):
    exchangeRates = {'USD': {'EUR': 0.93, 'GBP': 0.79, "USD":1}, 'EUR': {'USD': 1.07, 'GBP': 0.85, 'EUR':1}, 'GBP': {'USD': 1.25, 'EUR': 1.17, 'GBP':1}}

    exchangeRate = exchangeRates[senderCurrency][receiverCurrency]
    convertedAmount = float(amount) * exchangeRate
    response = {'senderAmount' : amount,
                'senderCurrency' : senderCurrency,
                'receiverAmount' : convertedAmount,
                'receiverCurrency' : receiverCurrency,
                'exchangeRate' : exchangeRate,
                'convertedAmount' : convertedAmount
                }
    return response.get('convertedAmount')