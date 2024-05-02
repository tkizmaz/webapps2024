from django.shortcuts import render
from .forms import RegisterForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import UserDetails
from api.views import convertCurrency

def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            convertedAmount = convertCurrency(request, 'GBP', form.cleaned_data.get("currency"), 1000)
            userDetails = UserDetails(user=user, currency=form.cleaned_data.get("currency"), balance=convertedAmount)
            userDetails.save()
            return redirect("login")
        else:
            messages.error(request, "Invalid username or password.")
    form = RegisterForm()
    return render(request, 'register.html', {"register_user": form})


def login_user(request):
    return render(request, "login.html")


def logout_user(request):
    logout(request)
    messages.error(request, 'Succesfully logged out!')
    redirect("login")

