from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal

class Transaction(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_transactions', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    timestamp = models.DateTimeField(auto_now_add=False)
    amountInSendersCurrency = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], null=True)
    amountInReceiversCurrency = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], null=True)
    senderCurrencySign = models.CharField(max_length=3, null=True)
    receiverCurrencySign = models.CharField(max_length=3, null=True)

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username} amount {self.amount}"

class MoneyRequest(models.Model):
    requestsSender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='request_sender', on_delete=models.CASCADE)
    requestReceiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='request_receiver', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    timestamp = models.DateTimeField(auto_now_add=False)
    accepted = models.BooleanField(default=False)
    moneyInRequestSendersCurrency = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], null=True)
    moneyInRequestReceiversCurrency = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], null=True)
    requestSenderCurrencySign = models.CharField(max_length=3, null=True)
    requestReceiverCurrencySign = models.CharField(max_length=3, null=True)

    def __str__(self):
        return f"Request from {self.requester.username} amount {self.amount}"
