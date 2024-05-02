from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from register.models import UserDetails
from staff.views import viewStaffHome
from .models import Transaction, MoneyRequest
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.contrib.auth.decorators import login_required
from api.views import convertCurrency
from thrift.TimestampHandlerClient.timestamphandlerclient import getTimeStampFromServer

currencySingDict = {
    "USD": "$",
    "EUR": "€",
    "GBP": "£"
}
# Create your views here.
@login_required
def viewHome(request):
    if request.user.is_staff:
        return viewStaffHome(request)
    requestCount = MoneyRequest.objects.filter(requestReceiver=request.user, accepted=False).count()
    paymentCount = Transaction.objects.filter(receiver=request.user).count()
    return render(request, "home.html", {'email': request.user.username, 'notificationCount': requestCount + paymentCount})

def transferDirectMoney(request):
    requests = MoneyRequest.objects.filter(requestReceiver=request.user, accepted=False)
    if request.method == "POST":
        email = request.POST.get("email")
        amount = Decimal(request.POST.get("amount", "0"))
        buttonType = request.POST.get('action','default')
        if buttonType == 'default':
            try:
                receiver = User.objects.get(email=email)
                if request.user.is_authenticated:
                    with transaction.atomic():
                        senderUserDetail = UserDetails.objects.get(user=request.user)
                        senderAmount = senderUserDetail.balance
                        if senderAmount >= amount:
                            senderUserDetail.balance -= amount
                            senderUserDetail.save()

                            convertedAmount = convertCurrency(request, senderUserDetail.currency, UserDetails.objects.get(user=receiver).currency, amount)
                            receiverUserDetail, created = UserDetails.objects.get_or_create(user=receiver, defaults={'balance': Decimal('0.00')})
                            receiverUserDetail.balance += Decimal(convertedAmount)
                            receiverUserDetail.save()

                            newTransaction = Transaction(sender=request.user, receiver=receiver, amount=amount, amountInSendersCurrency=amount, amountInReceiversCurrency=convertedAmount, timestamp=getTimeStampFromServer(), receiverCurrencySign=currencySingDict[UserDetails.objects.get(user=receiver).currency], senderCurrencySign=currencySingDict[senderUserDetail.currency])
                            newTransaction.save()
                            return render(request, "transaction.html", {'success': 'Transaction Successful','balance': UserDetails.objects.get(user=request.user).balance, 'requests':requests, 'currencySign': currencySingDict[UserDetails.objects.get(user=request.user).currency]})
                        else:
                            return render(request, "transaction.html", {'error': 'Insufficient balance','balance': UserDetails.objects.get(user=request.user).balance, 'requests':requests, 'currencySign': currencySingDict[UserDetails.objects.get(user=request.user).currency]})
            except User.DoesNotExist:
                return render(request, "transaction.html", {'error': 'No user with this email','balance': UserDetails.objects.get(user=request.user).balance, 'requests':requests, 'currencySign': currencySingDict[UserDetails.objects.get(user=request.user).currency]})
            except ObjectDoesNotExist:
                return render(request, "transaction.html", {'error': 'Operation failed','balance': UserDetails.objects.get(user=request.user).balance, 'requests':requests, 'currencySign': currencySingDict[UserDetails.objects.get(user=request.user).currency]})

        elif buttonType == 'accept':
            requestId = request.POST.get('requestId')
            try:
                moneyRequest = MoneyRequest.objects.get(id=requestId)
                if request.user == moneyRequest.requestReceiver:
                    with transaction.atomic():
                        moneySenderUserDetail = UserDetails.objects.get(user=request.user)
                        senderAmount = moneySenderUserDetail.balance
                        convertedAmount = convertCurrency(request, UserDetails.objects.get(user=moneyRequest.requestsSender).currency, moneySenderUserDetail.currency, moneyRequest.amount)
                        if senderAmount >= convertedAmount:
                            moneySenderUserDetail.balance -= Decimal(convertedAmount)
                            moneySenderUserDetail.save()

                            receiverUserDetail, created = UserDetails.objects.get_or_create(user=moneyRequest.requestsSender, defaults={'balance': Decimal('0.00')})
                            receiverUserDetail.balance += moneyRequest.amount
                            receiverUserDetail.save()
                            moneyRequest.accepted = True
                            newTransaction = Transaction(sender=request.user, receiver=receiverUserDetail.user, amount=moneyRequest.amount, amountInSendersCurrency=moneyRequest.moneyInRequestReceiversCurrency, amountInReceiversCurrency=moneyRequest.moneyInRequestSendersCurrency, timestamp=getTimeStampFromServer(), receiverCurrencySign=currencySingDict[receiverUserDetail.currency], senderCurrencySign=currencySingDict[moneySenderUserDetail.currency])
                            moneyRequest.save()
                            newTransaction.save()
                            return render(request, "transaction.html", {'success': 'Transaction Successful','balance': UserDetails.objects.get(user=request.user).balance, 'requests':requests, 'currencySign': currencySingDict[UserDetails.objects.get(user=request.user).currency]})
                        else:
                            return render(request, "transaction.html", {'error': 'Insufficient balance','balance': UserDetails.objects.get(user=request.user).balance, 'requests':requests, 'currencySign': currencySingDict[UserDetails.objects.get(user=request.user).currency]})
            except ObjectDoesNotExist:
                return render(request, "transaction.html", {'error': 'Operation failed','balance': UserDetails.objects.get(user=request.user).balance, 'requests':requests, 'currencySign': currencySingDict[UserDetails.objects.get(user=request.user).currency]})
        else:
            requestId = request.POST.get('requestId')
            try:
                moneyRequest = MoneyRequest.objects.get(id=requestId)
                if request.user == moneyRequest.requestReceiver:
                    moneyRequest.delete()
                    return render(request, "transaction.html", {'success': 'Request deleted','balance': UserDetails.objects.get(user=request.user).balance, 'requests':requests, 'currencySign': currencySingDict[UserDetails.objects.get(user=request.user).currency]})
            except ObjectDoesNotExist:
                return render(request, "transaction.html", {'error': 'Operation failed','balance': UserDetails.objects.get(user=request.user).balance, 'requests':requests, 'currencySign': currencySingDict[UserDetails.objects.get(user=request.user).currency]})

    return render(request, "transaction.html", {'balance': UserDetails.objects.get(user=request.user).balance, 'requests':requests, 'currencySign': currencySingDict[UserDetails.objects.get(user=request.user).currency]})

def requestMoney(request):
    requests = MoneyRequest.objects.filter(requestsSender=request.user, accepted=False)

    if request.method == "POST":
        email = request.POST.get("email")
        amount = Decimal(request.POST.get("amount", "0"))
        buttonType = request.POST.get('action','default')
        if buttonType == 'default':
            try:
                requestReceiver = User.objects.get(email=email)
                if request.user.is_authenticated:
                    newRequest = MoneyRequest(requestsSender=request.user, requestReceiver=requestReceiver, amount=amount, moneyInRequestSendersCurrency=amount, moneyInRequestReceiversCurrency=convertCurrency(request, UserDetails.objects.get(user=request.user).currency, UserDetails.objects.get(user=requestReceiver).currency, amount), timestamp=getTimeStampFromServer(), requestSenderCurrencySign=currencySingDict[UserDetails.objects.get(user=request.user).currency], reqestReceiverCurrencySign=currencySingDict[UserDetails.objects.get(user=requestReceiver).currency])
                    newRequest.save()
                    return render(request, "requestMoney.html", {'success': 'Request sent','balance': UserDetails.objects.get(user_id=request.user.id).balance, 'requests':requests, 'currencySign': currencySingDict[UserDetails.objects.get(user=request.user).currency]})
            except User.DoesNotExist:
                return render(request, "requestMoney.html", {'error': 'No user with this email','balance': UserDetails.objects.get(user_id=request.user.id).balance, 'requests':requests, 'currencySign': currencySingDict[UserDetails.objects.get(user=request.user).currency]})
            except ObjectDoesNotExist:
                return render(request, "requestMoney.html", {'error': 'Operation failed','balance': UserDetails.objects.get(user_id=request.user.id).balance, 'requests':requests, 'currencySign': currencySingDict[UserDetails.objects.get(user=request.user).currency]})
        elif buttonType == 'cancel':
            requestId = request.POST.get('requestId')
            try:
                moneyRequest = MoneyRequest.objects.get(id=requestId)
                if request.user == moneyRequest.requestsSender:
                    moneyRequest.delete()
                    return render(request, "requestMoney.html", {'success': 'Request deleted','balance': UserDetails.objects.get(user_id=request.user.id).balance, 'requests':requests, 'currencySign': currencySingDict[UserDetails.objects.get(user=request.user).currency]})
            except ObjectDoesNotExist:
                return render(request, "requestMoney.html", {'error': 'Operation failed','balance': UserDetails.objects.get(user_id=request.user.id).balance, 'requests':requests, 'currencySign': currencySingDict[UserDetails.objects.get(user=request.user).currency]})

    return render(request, "requestMoney.html", {'balance': UserDetails.objects.get(user_id=request.user.id).balance, 'requests':requests, 'currencySign': currencySingDict[UserDetails.objects.get(user=request.user).currency]})

def viewAccountInfo(request):
    userDetail = UserDetails.objects.get(user=request.user)
    return render(request, "accountInfo.html", {'userDetail': userDetail, 'balance': userDetail.balance, 'currencySign': currencySingDict[userDetail.currency]})

def viewTransactionHistory(request):
    transactionsMadeByYou = Transaction.objects.filter(sender=request.user).order_by('-timestamp')
    transactionsMadeToYou = Transaction.objects.filter(receiver=request.user).order_by('-timestamp')
    return render(request, "transactionHistory.html", {'transactionsMadeByYou': transactionsMadeByYou, 'transactionsMadeToYou': transactionsMadeToYou})

def viewNotifications(request):
    incomingTransactions = Transaction.objects.filter(receiver=request.user).order_by('-timestamp')
    incomingRequests = MoneyRequest.objects.filter(requestReceiver=request.user, accepted=False).order_by('-timestamp')
    return render(request, "notifications.html", {'transactions': incomingTransactions, 'currency': UserDetails.objects.get(user=request.user).currency, 'requests': incomingRequests})