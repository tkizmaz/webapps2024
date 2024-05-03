from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal

class UserDetails(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    currency = models.CharField(max_length=3, choices=(('GBP', 'GBP'), ('EUR', 'EUR'), ('USD', 'USD')))
    balance = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    email = models.EmailField(max_length=254, primary_key=True, unique=True, null=False, default='example@gmail.com')
    def __str__(self):
        return f"{self.user.username}'s profile"
